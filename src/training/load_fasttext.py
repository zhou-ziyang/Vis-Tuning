import fasttext

model = fasttext.load_model('model.bin')

words = model.get_words()

print(words)