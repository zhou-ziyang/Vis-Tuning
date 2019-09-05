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

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# for sentence in x_test:
#     print(' '.join([reverse_word_index.get(i, '?') for i in sentence]))
# print(y_test)

# print(' '.join([reverse_word_index.get(i, '?') for i in x_test[0]]))
# print(y_test[0])
# print(' '.join([reverse_word_index.get(i, '?') for i in x_test[1]]))
# print(y_test[1])

print('Pad sequences (samples x time)')
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_test shape:', x_test.shape)

model = load_model('../out/imdb.h5')



# score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
# print('Test score:', score)
# print('Test accuracy:', acc)

# pred = model.predict(x_test)
# print(pred.tolist())
# sentence = [1 if sent[0] > 0.5 else 0 for sent in pred]
# print(sentence)
# print(y_test.tolist())
#
# concat = zip(sentence, y_test.tolist())
# count = 0
# ones = 0
# for pair in concat:
#     count += 1
#     if pair[0] == pair[1]:
#         ones += 1
# print(ones/count)

comments = []
# positive
comments.append("<START> this film requires a lot of patience because it focuses on mood and character development "
                "the plot is very simple and many of the scenes take place on the same set in frances austen's the "
                "sandy dennis character apartment but the film builds to a disturbing climax br br the characters "
                "create an atmosphere rife with sexual tension and psychological trickery it's very interesting that "
                "robert altman directed this considering the style and structure of his other films still the "
                "trademark altman audio style is evident here and there i think what really makes this film work is "
                "the brilliant performance by sandy dennis it's definitely one of her darker characters but she plays "
                "it so perfectly and convincingly that it's scary michael burns does a good job as the mute young man "
                "regular altman player michael murphy has a small part the <UNK> moody set fits the content of the "
                "story very well in short this movie is a powerful study of loneliness sexual repression and "
                "desperation be patient <UNK> up the atmosphere and pay attention to the wonderfully written script "
                "br br i praise robert altman this is one of his many films that deals with unconventional "
                "fascinating subject matter this film is disturbing but it's sincere and it's sure to elicit a strong "
                "emotional response from the viewer if you want to see an unusual film some might even say bizarre "
                "this is worth the time br br unfortunately it's very difficult to find in video stores you may have "
                "to buy it off the internet")
# negative
comments.append("<START> please give this one a miss br br kristy swanson and the rest of the cast rendered terrible "
                "performances the show is flat flat flat br br i don't know how michael madison could have allowed "
                "this one on his plate he almost seemed to know this wasn't going to work out and his performance was "
                "quite lacklustre so all you madison fans give this a miss")

comments_new = []

for comment in comments:
    comment_split = comment.split(sep=" ")
    comment_list = [word_index.get(i, 2) for i in comment_split]
    print(comment_list)
    comments_new.append(comment_list)

x_comment = sequence.pad_sequences(np.array(comments_new), maxlen=maxlen)

# print(x_comment)
pred2 = model.predict(x_comment)
print(pred2.tolist())
sentence2 = [1 if sent[0] > 0.5 else 0 for sent in pred2]
print(sentence2)
# print(y_test.tolist())

print(model['this'])
