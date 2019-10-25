import codecs
import json
import multiprocessing
import os
import re

import numpy as np
import time

import fasttext
from scipy.stats import stats
from sklearn.metrics import r2_score, confusion_matrix

from modules.event import Event


def print_results(n, p, r):
    print("N\t" + str(n))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))


def result(n, p, r):
    return "N\t" + str(n) + ", P@{}\t{:.3f}".format(1, p) + ", R@{}\t{:.3f}".format(1, r)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  NEW FOLDER  ---")
        print("---  FINISH  ---")
    else:
        print("---  Folder already exists!  ---")


def prediction_mean(prediction):
    rating_dict = dict(zip(prediction[0], prediction[1]))
    mean = 0
    for i in range(10):
        try:
            mean += rating_dict['__label__' + str(i + 1)] * (i + 1)
        except KeyError:
            pass
    mean_score = int(round(mean))
    return mean_score


class FasttextImdb:
    def __init__(self, group, sbj_id):
        self.sbj_id = sbj_id
        self.observer = None
        self.group = group
        self.read_path = "static/pipe/fasttext.pipe"
        self.update = {}
        self.training_round = 0
        self.kwargs = {}
        self.model = None
        self.model_aux = None
        self.directory = ""
        self.pipe = None
        self.read_thread = None
        self.write_thread = None
        self.rf = None
        self.maxlen = 350

    def train(self, training_round, observer, kwargs=None):
        self.training_round = training_round
        self.observer = observer
        self.kwargs = kwargs

        # Event('append', "Initializing...")
        # print("Initializing...")
        # pool0 = multiprocessing.Pool(2)
        #
        # pool0.apply_async(self.start_training_aux, ())
        # pool0.apply_async(self.start_reading, (False,))
        #
        # pool0.close()
        # pool0.join()

        pool = multiprocessing.Pool(2)
        pool.apply_async(self.start_training, ())
        pool.apply_async(self.start_reading, (True,))

        pool.close()
        pool.join()

    def start_training(self):
        print("writing thread is on")
        self.model = fasttext.train_supervised(input="static/data/imdb/dataset/imdb.train", **self.kwargs)
        self.save()
        # self.running = False

    def save(self):
        self.directory = "static/out/" + self.sbj_id + "/" + str(self.training_round)
        mkdir(self.directory)
        self.model.save_model(self.directory + "/model.bin")
        # print_results(*self.model.test('static/data/imdb/dataset/imdb.dev', 1))

        if self.observer is not None:
            self.evaluate()

        file = codecs.open(self.directory + "/model.vec", "w")
        file_dict = codecs.open(self.directory + "/dict.csv", "w")
        words = self.model.get_words()
        file.write(str(len(words)) + " " + str(self.model.get_dimension()) + "\n")
        file_dict.write("word,rating" + "\n")
        for word in words:
            word_vector = " ".join([str(vector) for vector in self.model.get_word_vector(word)])
            file.write(word + " " + word_vector + "\n")
            # word_label = self.model.predict(word, 1)[0][0].split("__label__")[1]
            word_prediction = self.model.predict(word, 10)
            word_score = prediction_mean(word_prediction)
            # word_score = int(word_label)
            if word_score < 4 or word_score > 7:
                file_dict.write(word + "," + str(word_score) + "\n")
        file.close()
        file_dict.close()

        file_dict.write(str(len(words)) + " " + str(self.model.get_dimension()) + "\n")

    # def start_training_aux(self):
    #     print("writing thread is on")
    #     self.model_aux = fasttext.train_supervised(input="static/data/imdb/dataset/imdb_bi.train", **self.kwargs)
    #     self.save_aux()

    # def save_aux(self):
    #     self.directory = "static/out/" + self.sbj_id + "/" + str(self.training_round)
    #     mkdir(self.directory)
    #     self.model_aux.save_model(self.directory + "/model_aux.bin")
    #
    #     file2 = codecs.open(self.directory + "/model_aux.vec", "w")
    #     words2 = self.model_aux.get_words()
    #     file2.write(str(len(words2)) + " " + str(self.model_aux.get_dimension()) + "\n")
    #     for word in words2:
    #         word_vector = " ".join([str(vector) for vector in self.model_aux.get_word_vector(word)])
    #         file2.write(word + " " + word_vector + "\n")
    #     file2.close()

    def evaluate(self):
        Event('append', str({"evaluating": "Saving..."}))
        predictions = []
        truths = []
        with codecs.open("static/data/imdb/dataset/imdb.dev", 'r') as f_in:
            tuples = [line.split(' ', maxsplit=1) for line in f_in]
            # file = codecs.open(self.directory + "/result.txt", "w")
            file = codecs.open(self.directory + "/model_sentence.vec", "w")
            for tuple in tuples:
                try:
                    label, sent = tuple
                except Exception:
                    pass
                truth = label.split('__label__')
                truths.append(int(truth[1]))

                words_no_Punc = re.sub(r'[^\w\s]', ' ', sent.lower())
                words_no_double_blank = re.sub(r'\s\s+', ' ', words_no_Punc)
                words_no_newline = re.sub(r' newline ', ' <NEWLINE> ', words_no_double_blank).split(" ")
                sent_processed = " ".join(words_no_newline[:self.maxlen]).strip()

                prediction = self.model.predict(sent_processed, 10)

                # rating = prediction[0][0].split('__label__')
                # predictions.append(int(rating[1]))

                mean_score = prediction_mean(prediction)
                predictions.append(mean_score)

                # file.write("Truth: " + str(truth) + "\n" + "Prediction: " + str(prediction) + "\n" + "Mean: " + str(
                #     mean_score) + "\n")
                # file.write("Truth: " + str(truth) + "\n" + "Prediction: " + str(prediction) + "\n")

                vector = " ".join([str(num) for num in self.model.get_sentence_vector(sent.strip())])
                file.write(label + ", __label__" + str(mean_score) + ", " + str(vector) + ", " + sent.strip() + "\n")

            # file.close()
            file.close()

        Event('append', str({"evaluating": "Evaluating..."}))

        r2 = str(r2_score(truths, predictions))
        Event('append', str({"evaluating": "R2-Score: " + r2}))
        file_log = codecs.open(self.directory + "/log.txt", "w")
        file_log.write(str(time.time()) + " " + r2)

        # Event('append', str({"evaluating": "t-statistic: " + str(stats.ttest_rel(truths, predictions).statistic)}))
        # Event('append', str({"evaluating": "p-value: " + str(stats.ttest_rel(truths, predictions).pvalue)}))

        Event('append', str({"evaluating": "Plotting confusion matrix..."}))
        self.plot_cm(truths, predictions)
        Event('append', str({"evaluating": "Done."}))

        if self.group != 1:
            Event('append', str({"evaluating": "Plotting scatter..."}))
            self.plot_scatter()
            Event('append', str({"evaluating": "Done."}))

    def plot_cm(self, truths, predictions):
        cm = str(confusion_matrix(truths, predictions).tolist())
        # print(cm)
        Event('append', json.dumps({"cm": cm}))

    def plot_scatter(self):
        labels_plot = []
        pred_plot = []
        vecs_plot = []
        sents_plot = []

        labels = []
        preds = []
        embeddings = []
        sentences = []

        with codecs.open(self.directory + "/model_sentence.vec", 'r', 'utf-8') as f_in:
            tuples = [line.split(', ', maxsplit=3) for line in f_in]
            for tuple in tuples:
                try:
                    label, pred, embed, sentence = tuple
                    # print(label, pred)
                except Exception:
                    pass
                labels.append(label)
                preds.append(pred)
                embeddings.append(embed)
                sentences.append(sentence.strip())

        for i in range(1, len(labels)):  # Usually skip first 10 words because they might be garbage values.
            labels_plot.append(labels[i])
            pred_plot.append(preds[i])
            x = embeddings[i]
            vecs_plot.append(np.fromstring(x, dtype='float32', sep=' '))
            sents_plot.append(sentences[i])

        U, s, Vh = np.linalg.svd(vecs_plot, full_matrices=False)

        file = codecs.open(self.directory + "/scatter.csv", "w")
        file.write(','.join(["label", "pred", "x", "y", "sentence"]) + "\n")
        for i in range(len(labels_plot)):
            score = labels_plot[i].split("__label__")[1]
            prediction = pred_plot[i].split("__label__")[1]
            # print(score, prediction)
            sent1 = re.sub(r'&amp;', r'&', sents_plot[i])
            sent2 = re.sub(r'(?<! )(?=[.,!?()"¨:*&\'/|+_#[\-])|(?<=[.,!?()"¨:*&\'/|+_#[\-])(?! )', r'<BREAK>', sent1)
            sent3 = re.sub(r'"|¨', r'&quot;', sent2)
            file.write(','.join([score, prediction, str(U[i, 0]), str(U[i, 1]), '\"' + sent3 + '\"']) + "\n")
        file.close()

        # U, s, Vh = np.linalg.svd(embeddings, full_matrices=False)
        #
        # file = codecs.open(self.directory + "/scatter.csv", "w")
        # file.write(','.join(["label", "pred", "x", "y", "sentence"]) + "\n")
        # for i in range(len(labels)):
        #     score = labels[i].split("__label__")[1]
        #     prediction = preds[i].split("__label__")[1]
        #     # print(score, prediction)
        #     sent1 = re.sub(r'&amp;', r'&', sentences[i])
        #     sent2 = re.sub(r'(?<! )(?=[.,!?()"¨:*&\'/|+_#[\-])|(?<=[.,!?()"¨:*&\'/|+_#[\-])(?! )', r'<BREAK>', sent1)
        #     sent3 = re.sub(r'"|¨', r'&quot;', sent2)
        #     file.write(','.join([score, prediction, str(U[i, 0]), str(U[i, 1]), '\"' + sent3 + '\"']) + "\n")
        # file.close()

        Event('append', json.dumps({"scatter": ""}))

    def make(self):
        try:
            os.mkfifo(self.read_path)
        except OSError as e:
            print("mkfifo error", e)

    def createPipe(self):
        print("reading thread is on")
        self.rf = os.open(self.read_path, os.O_RDONLY)
        print("os.open finished")

    def openPipe(self, reaction):
        while True:
            data = os.read(self.rf, 1024)
            if reaction:
                print(data)
                if len(data) != 0:
                    Event('append', str(data)[2:-5])
                print(str(data)[34:37])
            if str(data)[34:37] == "100":
                self.rf.close()
                break

    def start_reading(self, reaction):
        # print(reaction)
        self.createPipe()
        self.openPipe(reaction)
