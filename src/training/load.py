from keras.datasets import imdb
from keras.engine.saving import load_model
from keras.preprocessing import sequence
import numpy as np

max_features = 20000
batch_size = 32
maxlen = 400

# f = np.load("imdb.npz")
# x_test, y_test = f['x_test'], f['y_test']
# f.close()

# save np.load
np_load_old = np.load
# modify the default parameters of np.load
np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
# call load_data with allow_pickle implicitly set to true
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
# restore np.load for future normal usage
np.load = np_load_old

word_index = imdb.get_word_index()
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

# reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
#
# for sentence in x_test:
#     print(' '.join([reverse_word_index.get(i, '?') for i in sentence]))

# print(y_test)

print('Pad sequences (samples x time)')
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_test shape:', x_test.shape)

model = load_model('imdb.h5')

# score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
# print('Test score:', score)
# print('Test accuracy:', acc)

pred = model.predict(x_test)
print(pred.tolist())
sentence = [1 if sent[0] > 0.5 else 0 for sent in pred]
print(sentence)
print(y_test.tolist())

concat = zip(sentence, y_test.tolist())
count = 0
ones = 0
for pair in concat:
    count += 1
    if pair[0] == pair[1]:
        ones += 1
print(ones/count)

comment = "<START> allegedly the true story of de the eldest daughter of the catholic queen <UNK> yes the same who " \
          "funded <UNK> expedition the film charts the progress and <UNK> of her morbid obsession with her husband " \
          "the philip of austria known as the handsome and played in a rather manner by italian hunk <UNK> at his " \
          "most and <UNK> here this is a groan familiar story of late <UNK> c early 16th c intrigue betrayal and " \
          "<UNK> ripping it <UNK> destructive lust from start to finish but while la <UNK> <UNK> succeeds in making " \
          "cruel sensuality and ruthless cut throat intrigue entertaining to watch la just doesn't pull off it just " \
          "ends up feeling like a big budgeted soap opera with below average lazy or over keen acting looks " \
          "positively bored and <UNK> de in the title role   though to be fair she may mature into a proper talent   " \
          "just seems to be trying too hard switching back and fourth from two dimensional horny looking to spoilt " \
          "teenage hysterics all the way through some of the supporting cast are ok with the exception of another " \
          "italian pin up voluptuous and beautiful but really no actress to speak of i couldn't in fact bring myself " \
          "to feel any concern towards any character nor for that matter did i feel strongly in a negative way " \
          "against any of the supposed villains what a waste of a substantial film budget this one sadly is just so " \
          "<UNK> and deja vu nodding to other films in the genre rather than to its source material history for " \
          "inspiration it seems to me that such a fascinating and complex historic era deserved a far superior film " \
          "maker to evoke it"
comment = comment.split(sep=" ")
comment = [word_index.get(i, 2) for i in comment]
x_comment = sequence.pad_sequences(np.array([comment]), maxlen=maxlen)
