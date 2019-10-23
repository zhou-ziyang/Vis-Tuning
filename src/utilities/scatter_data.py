import numpy as np
import codecs  # To open the file in specific mode

labels_plot = []
pred_plot = []
vecs_plot = []
sents_plot = []

labels = []
preds = []
embeddings = []
sentences = []

with codecs.open('IMDB_Crawled/model_sentence_Pre.vec', 'r', 'utf-8') as f_in:
    # vocabulary, wv = zip(*[line.strip().split(' ', maxsplit=1) for line in f_in])
    tuples = [line.split(',', maxsplit=3) for line in f_in]
    for tuple in tuples:
        try:
            label, pred, embed, sentence = tuple
        except Exception:
            pass
        labels.append(label)
        preds.append(pred)
        embeddings.append(embed)
        sentences.append(sentence.strip())

for i in range(10, len(labels)):  # Usually skip first 10 words becuase they might be garbage values.
    labels_plot.append(labels[i])
    pred_plot.append(preds[i])
    x = embeddings[i]
    vecs_plot.append(np.fromstring(x, dtype='float32', sep=' '))
    sents_plot.append(sentences[i])

U, s, Vh = np.linalg.svd(vecs_plot, full_matrices=False)

file = codecs.open("../static/data/scatter.csv", "w")
file.write(','.join(["label", "pred", "x", "y", "sentence"]) + "\n")
for i in range(len(labels_plot)):
    score = labels_plot[i].split("__label__")[1]
    prediction = pred_plot[i].split("__label__")[1]
    file.write(','.join([score, prediction, str(U[i, 0]), str(U[i, 1]), sents_plot[i]]) + "\n")
file.close()
