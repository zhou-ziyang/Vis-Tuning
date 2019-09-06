import codecs
import fasttext

model = fasttext.load_model('model.bin')

file = open("model_sent.vec", "w")
with codecs.open('imdb.train', 'r', 'utf-8') as f_in:
    # label, sentence = zip(*[line.strip().split(' ', maxsplit=1) for line in f_in])
    pairs = [line.split(' ', maxsplit=1) for line in f_in]
    for pair in pairs:
        try:
            label, sentence = pair
        except Exception:
            pass

        print(sentence)
        vector = " ".join([str(num) for num in model.get_sentence_vector(sentence[:-1])])
        print(vector)
        file.write(label + " " + str(vector) + "\n")

# for word in model.get_words():
#     if word is not " ":
#         vector = " ".join([str(num) for num in model.get_word_vector(word)])
#         file.write(word + " " + vector + "\n")
file.close()
