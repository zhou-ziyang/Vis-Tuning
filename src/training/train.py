from training.lstm import RNN
from training.mnist_cnn import CNN


class Train:
    def __init__(self):
        self.rnn = RNN()

    def start(self, units, dropout, recurrent_dropout, batch_size, epochs, logger):
        logger.observe('append', logger.append)
        self.rnn.train(units, dropout, recurrent_dropout, batch_size, epochs, logger)
