import fasttext


model = fasttext.train_supervised(input="IMDB_Crawled/imdb.train", wordNgrams=1, epoch=35)
model.save_model("IMDB_Crawled/model.bin")


def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

print_results(*model.test('IMDB_Crawled/imdb.dev', 1))

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

# print(model.predict(comments[0]))

# vector = model.get_sentence_vector(comments[0])
# print(vector)

file = open("IMDB_Crawled/model.vec", "w")
file.write(str(len(model.get_words())) + " " + str(model.get_dimension()) + "\n")
for word in model.get_words():
    if word is not " ":
        vector = " ".join([str(num) for num in model.get_word_vector(word)])
        file.write(word + " " + vector + "\n")
file.close()
