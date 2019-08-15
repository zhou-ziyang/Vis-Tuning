from training.lstm import RNN


class Start:
    # train = '/Users/zhouziyang/Documents/LMU/Studium/Informatik/Bachelorarbeit/Flask/test/training/relations' \
    #         '/train_relations.tsv'
    # dev = '/Users/zhouziyang/Documents/LMU/Studium/Informatik/Bachelorarbeit/Flask/test/training/relations' \
    #       '/dev_relations.tsv'
    # pred = '/Users/zhouziyang/Documents/LMU/Studium/Informatik/Bachelorarbeit/Flask/test/training/relations' \
    #        '/prediction.tsv'
    observer = None
    # units, dropout, recurrent_dropout, batch_size, epochs = 64, 0.5, 0.5, 64, 10

    def __init__(self, observer):
        # self.units, self.dropout, self.recurrent_dropout, self.batch_size, self.epochs = units, dropout, recurrent_dropout, batch_size, epochs
        self.observer = observer

    def start(self, units, dropout, recurrent_dropout, batch_size, epochs, observer):
        predictor = RNN()
        predictor.train(units, dropout, recurrent_dropout, batch_size, epochs, observer)
