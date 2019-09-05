import numpy as np

from keras.datasets import imdb

max_features = 20000
maxlen = 400

# save np.load
np_load_old = np.load
# modify the default parameters of np.load
np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
# call load_data with allow_pickle implicitly set to true
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features, maxlen=maxlen)
# restore np.load for future normal usage
np.load = np_load_old

training_set = []

word_index = imdb.get_word_index()
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

for words, label in zip(x_train, y_train):
    sentence = ' '.join([reverse_word_index.get(i, '?') for i in words])
    # sentence = ' '.join(str(words))
    aspect = "negative" if label == 0 else "positive"
    seq = ("__label__", aspect, " ", sentence)
    entry = "".join(seq)
    training_set.append(entry)

file = open("imdb2.train", "w")
for training_data in training_set:
    file.write(training_data)
    file.write("\n")
file.close()


for words, label in zip(x_test, y_test):
    sentence = ' '.join([reverse_word_index.get(i, '?') for i in words])
    # sentence = ' '.join(str(words))
    aspect = "negative" if label == 0 else "positive"
    seq = ("__label__", aspect, " ", sentence)
    entry = "".join(seq)
    training_set.append(entry)

file = open("imdb.valid", "w")
for training_data in training_set:
    file.write(training_data)
    file.write("\n")
file.close()
