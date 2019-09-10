import codecs
import matplotlib.pyplot as plt
import fasttext
import numpy as np
import scipy as sp
from sklearn.metrics import r2_score

model = fasttext.load_model('IMDB_Crawled/model.bin')

def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

# print_results(*model.test('IMDB_Rating_Data/imdb_rating.test', 1))

comments = []
# 2
# comments.append("A remake can be successful. An adaptation can be successful. It isn't relevant whether its a remake "
#                 "or an adaptation.<br /><br />A good movie is a good movie and a poor movie is a poor movie, "
#                 "regardless.<br /><br />Sarkar, I am afraid, was a very poor movie. First of all, just by making "
#                 "characters look dangerous, or macho, they don't bring in an aura about them.<br /><br />What was so "
#                 "brilliant about Nagre(Amitabh Bacchan's character) that we should have been in aura of his 'power' "
#                 "and what showed the 'benevolence' of the character? Nothing.<br /><br />This fact was said by a "
#                 "commentator and Amitabh kept giving facial expressions. Now Amitabh can give brilliant facial "
#                 "expressions but why should it mean any thing if there is no history or story to go with it.<br /><br "
#                 "/>There wasn't proper charecterisation of the characters who worked under 'sarkar' too. Just because "
#                 "a man had spectacles, why should we assume he is wise. ] The flow of the movie was generally "
#                 "dullbecause scenes from the Godfather were created (like the policeman slapping Abhishek Bacchan), "
#                 "the older brother being killed by Abhishek (like Fredo was killed on instructions of Pacino) but too "
#                 "much was sought to be packed into the movie with too little story and depth to go with it. That was "
#                 "indeed the problem.<br /><br />If you try to pack 3 hours of intricate detail like a Godfather in 2 "
#                 "hours and that too with few dialogues, what you get is a highlights show from a cricket match, "
#                 "never making the full impact watching a full match will make.")

# 4
comments.append("\"Hardbodies 2\" is harmless, aimless and plot less. I would add \"brainless\" to that list, "
                "but the movie-within-a-movie gimmick, although not done very well, helps it to narrowly escape that "
                "label. The scenery has changed from the California beaches to the Greek islands, and the only "
                "returning cast members from the first film are Sorrells Pickard (the bearded guy) and Roberta "
                "Collins (who at one point falls into a mud pit, bringing back memories of her classic catfight with "
                "Pam Grier in \"The Big Doll House\"). All the other actors are new, but apparently Brad Zutaut is "
                "supposed to be playing the same character (Scotty) as Grant Cramer did in \"Hardbodies\". This "
                "sequel lacks the energy and appeal of the first movie, and doesn't come close to matching it in the "
                "\"hotness\" department, either. Of course Brenda Bakke and Fabiana Udenio are both very pretty, "
                "but the Teal Roberts - Cindy Silver - Kristi Somers team is unbeatable. \"Hardbodies 2\" is not the "
                "worst of its kind by any means, but if you only want to see one of these movies, the original is the "
                "one to get. (*1/2)")



# print(model.predict(comments[0], 2))


predictions = []
truths = []

with open('IMDB_Crawled/imdb.valid', 'r') as f_in:
    # vocabulary, wv = zip(*[line.strip().split(' ', maxsplit=1) for line in f_in])
    pairs = [line.split(' ', maxsplit=1) for line in f_in]
    file = open("IMDB_Crawled/result", "w")
    for pair in pairs:
        try:
            a, b = pair
        except Exception:
            pass
        truth = a.split('__label__')
        truths.append(int(truth[1]))
        prediction = model.predict(b[:-1], 8)

        rating = prediction[0][0].split('__label__')
        predictions.append(int(rating[1]))

        # rating_dict = dict(zip(prediction[0], prediction[1]))
        # mean = 0
        # for i in range(10):
        #     try:
        #         mean += rating_dict['__label__' + str(i + 1)] * (i + 1)
        #     except KeyError:
        #         pass
        # mean_score = mean
        # predictions.append(mean_score)

        # file.write("Truth: " + str(truth) + "\n" + "Prediction: " + str(prediction) + "\n" + "Mean: " + str(mean_score) + "\n")
        file.write("Truth: " + str(truth) + "\n" + "Prediction: " + str(prediction) + "\n")

    file.close()

accuracy = map('dist', zip(predictions, truths))
# print(np.array(list(map(lambda x, y: abs(x - y), predictions, truths))).mean())
# print(*zip(truths, predictions))
print(np.mean((np.array(predictions) - np.array(truths)) ** 2))
print(r2_score(truths, predictions))

fig = plt.figure(figsize=(8, 8))

ax1 = fig.add_subplot(2, 1, 1)
ax1.hist(truths, bins=11, range=(0, 11), color='g')

# rounded_predictions = list(map(lambda x: round(x, 0), predictions))
ax2 = fig.add_subplot(2, 1, 2)
ax2.hist(predictions, bins=11, range=(0, 11), color='g')

plt.show()


