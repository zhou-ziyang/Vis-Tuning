import codecs
import fasttext
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

model = fasttext.load_model('model.bin')

scores = []

file = open("model_sentence_score.vec", "w")

with codecs.open('imdb.train', 'r', 'utf-8') as f_in:
    # label, sentence = zip(*[line.strip().split(' ', maxsplit=1) for line in f_in])
    pairs = [line.split(' ', maxsplit=1) for line in f_in]
    for pair in pairs:
        try:
            # label, sentence = pair
            _, sentence = pair
        except Exception:
            pass

        # print(sentence)
        vector = " ".join([str(num) for num in model.get_sentence_vector(sentence[:-1])])
        # print(vector)
        # file.write(label + " " + str(vector) + "\n")
        predict = model.predict(sentence[:-1], k=2)
        index = predict[0].index('__label__positive')
        score = round(predict[1][index], 2)
        scores.append(predict[1][index])
        # print(score)
        file.write(str(score) + " " + str(vector) + "\n")

file.close()

# score_range = np.arange(0, 1.1, 0.1)
# zeros = np.zeros(len(score_range))
# score_dict = dict(np.round(np.column_stack((score_range, zeros)), 2))

# for score in scores:
#     score_dict[score] += 1

# print(score_dict)

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(2, 1, 1)
ax1.hist(scores, bins=20, color='g')

# scores_sort = sorted(scores)
# # print(scores_sort)
# quantile = np.linspace(0, 1, len(scores_sort))
# normal = np.random.normal(loc=0.5, scale=1.0, size=len(scores_sort))

# ax2 = fig2.add_subplot(2, 1, 2)
# ax2.scatter(score_dict.keys(), score_dict.values())

plt.show()
