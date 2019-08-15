"""Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
"""
import json

import keras
from keras.models import Sequential
from keras.layers import np, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as k

from training.send_callback import SendCallback


class CNN:
    model = Sequential()
    batch_size = 128
    num_classes = 10
    epochs = 12
    x_train, y_train, x_test, y_test = None, None, None, None

    def __init__(self):

        # input image dimensions
        img_rows, img_cols = 28, 28

        # the data, split between train and test sets
        # (x_train, y_train), (x_test, y_test) = mnist.load_data()

        f = np.load("/Users/zhouziyang/Documents/LMU/Studium/Informatik/Bachelorarbeit/Flask/test/static/mnist.npz")
        self.x_train, self.y_train = f['x_train'], f['y_train']
        self.x_test, self.y_test = f['x_test'], f['y_test']
        f.close()

        if k.image_data_format() == 'channels_first':
            self.x_train = self.x_train.reshape(self.x_train.shape[0], 1, img_rows, img_cols)
            self.x_test = self.x_test.reshape(self.x_test.shape[0], 1, img_rows, img_cols)
            input_shape = [1, img_rows, img_cols]
        else:
            self.x_train = self.x_train.reshape(self.x_train.shape[0], img_rows, img_cols, 1)
            self.x_test = self.x_test.reshape(self.x_test.shape[0], img_rows, img_cols, 1)
            input_shape = [img_rows, img_cols, 1]

        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255
        print('x_train shape:', self.x_train.shape)
        print(self.x_train.shape[0], 'train samples')
        print(self.x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(self.y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(self.y_test, self.num_classes)



        # self.model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
        # self.model.add(Conv2D(64, (3, 3), activation='relu'))
        # self.model.add(MaxPooling2D(pool_size=(2, 2)))
        # self.model.add(Dropout(0.25))
        # self.model.add(Flatten())
        # self.model.add(Dense(128, activation='relu'))
        # self.model.add(Dropout(0.5))
        # self.model.add(Dense(self.num_classes, activation='softmax'))

    def addLayerFromJson(self, args):
        layer_form = args["layer_type"]
        kwargs = args["args"]
        self.model.add(eval(layer_form)(**kwargs))

    def addLayerFromStr(self, str_args):
        args = json.loads(str_args)
        self.addLayerFromJson(args)

    def train(self, conf, logger=None):
        args = json.loads(conf)
        print(args)

        for key in args:
            print(key)
            self.addLayerFromJson(args[key])

        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=keras.optimizers.Adadelta(),
                           metrics=['accuracy'])
        call_back = SendCallback(observer=logger)
        self.model.fit(self.x_train, self.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=1,
                       validation_data=(self.x_test, self.y_test),
                       callbacks=[call_back])
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])


if __name__ == "__main__":
    cnn = CNN()
    cnn.train()
