from modules.fasttext_imdb import FasttextImdb


class Training:
    def __init__(self, group, subj_id):
        self.fasttext = FasttextImdb(group, subj_id)

    def start(self, training_round, observer, kwargs):
        observer.observe('append', observer.append)
        self.fasttext.train(training_round, observer, kwargs)

    def stop(self):
        self.fasttext.stop()
