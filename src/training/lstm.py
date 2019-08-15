'''
#Trains an LSTM model on the IMDB sentiment classification task.
The dataset is actually too small for LSTM to be of any advantage
compared to simpler, much faster methods such as TF-IDF + LogReg.
**Notes**
- RNNs are tricky. Choice of batch size is important,
choice of loss and optimizer is critical, etc.
Some configurations won't converge.
- LSTM loss decrease patterns during training can be quite different
from what you see with CNNs/MLPs/etc.
'''
from __future__ import print_function

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, GRU, LSTM
from keras.datasets import imdb

from training.send_callback import SendCallback


class RNN:
    model = Sequential()
    max_features = 20000
    # cut texts after this number of words (among top max_features most common words)
    maxlen = 80
    # batch_size = 32
    x_train, y_train, x_test, y_test = None, None, None, None
    # units, dropout, recurrent_dropout, batch_size, epochs = 0, 0, 0, 0, 0
    logger = None

    def __init__(self):
        # self.units, self.dropout, self.recurrent_dropout, self.batch_size, self.epochs, self.logger = units, dropout, recurrent_dropout, batch_size, epochs, observer
        print('Loading data...')
        (self.x_train, self.y_train), (self.x_test, self.y_test) = imdb.load_data(num_words=self.max_features)
        print(len(self.x_train), 'train sequences')
        print(len(self.x_test), 'test sequences')

        word_index = imdb.get_word_index()
        word_index = {k: (v + 3) for k, v in word_index.items()}
        word_index["<PAD>"] = 0
        word_index["<START>"] = 1
        word_index["<UNK>"] = 2  # unknown
        word_index["<UNUSED>"] = 3

        # reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

        # for sentence in x_train:
        #     print(' '.join([reverse_word_index.get(i, '?') for i in sentence]))

        # for x in y_train:
        #     print(x)

        print('Pad sequences (samples x time)')
        self.x_train = sequence.pad_sequences(self.x_train, maxlen=self.maxlen)
        self.x_test = sequence.pad_sequences(self.x_test, maxlen=self.maxlen)
        print('x_train shape:', self.x_train.shape)
        print('x_test shape:', self.x_test.shape)

    def train(self, units, dropout, recurrent_dropout, batch_size, epochs, logger=None):
        # print(units, dropout, recurrent_dropout, batch_size, epochs)
        print('Build model...')
        self.model.add(Embedding(self.max_features, units))
        self.model.add(GRU(units, dropout=dropout, recurrent_dropout=recurrent_dropout))
        self.model.add(Dense(1, activation='sigmoid'))

        # try using different optimizers and different optimizer configs
        self.model.compile(loss='binary_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy'])

        print('Train...')
        call_back = SendCallback(observer=logger)
        self.model.fit(self.x_train, self.y_train,
                       batch_size=batch_size,
                       epochs=epochs,
                       validation_data=(self.x_test, self.y_test),
                       callbacks=[call_back])
        score, acc = self.model.evaluate(self.x_test, self.y_test, batch_size=batch_size)
        print('Test score:', score)
        print('Test accuracy:', acc)


if __name__ == "__main__":
    rnn = RNN(64, 0.5, 0.5, 64, 10)
    rnn.train()
