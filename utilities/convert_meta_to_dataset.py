import random
import re
import codecs

train_set = []
dev_set = []
test_set = []
percentage = [0.6, 0.8, 0.9]
maxlen = 350
file1 = codecs.open("../static/data/imdb/dataset/imdb.train", "w")
file2 = codecs.open("../static/data/imdb/dataset/imdb.dev", "w")
file3 = codecs.open("../static/data/imdb/dataset/imdb.test", "w")
file4 = codecs.open("../static/data/imdb/dataset/imdb_bi.train", "w")

for i in range(10):
    rating = i + 1
    with codecs.open("../static/data/imdb/meta/imdb_review_" + str(rating) + ".txt", "r") as f_in:
        review_list = [line for line in f_in]
    number = len(review_list)
    train_set += review_list[:int(number * percentage[0])]
    dev_set += review_list[int(number * percentage[0]):int(number * percentage[1])]
    test_set += review_list[int(number * percentage[1]):]

random.shuffle(train_set)
random.shuffle(dev_set)
random.shuffle(test_set)

for train_data in train_set:
    words_no_Punc = re.sub(r'[^\w\s]', ' ', train_data.lower())
    words_no_double_blank = re.sub(r'\s\s+', ' ', words_no_Punc)
    words_no_newline = re.sub(r' newline ', ' <NEWLINE> ', words_no_double_blank).split(" ")
    s = " ".join(words_no_newline[:maxlen]).strip()
    file1.write(s + "\n")

    train_data_split = s.split(" ", maxsplit=1)
    score = int(train_data_split[0].split("__label__", maxsplit=1)[1])
    if score >= 6:
        file4.write("__label__pos " + train_data_split[1].strip() + "\n")
    else:
        file4.write("__label__neg " + train_data_split[1].strip() + "\n")

for dev_data in dev_set:
    # words_no_Punc = re.sub(r'[^\w\s]', ' ', dev_data.lower())
    # words_no_double_blank = re.sub(r'\s\s+', ' ', words_no_Punc)
    # words_no_newline = re.sub(r' newline ', ' <NEWLINE> ', words_no_double_blank).split(" ")
    # s = " ".join(words_no_newline[:maxlen]).strip()
    file2.write(dev_data.strip() + "\n")

    # dev_data_split = dev_data.split(" ", maxsplit=1)
    # score = int(dev_data_split[0].split("__label__", maxsplit=1)[1])
    # if score >= 5:
    #     file4.write("__label__pos " + dev_data_split[1].strip() + "\n")
    # else:
    #     file4.write("__label__neg " + dev_data_split[1].strip() + "\n")

for test_data in test_set:
    # words_no_Punc = re.sub(r'[^\w\s]', ' ', test_data.lower())
    # words_no_double_blank = re.sub(r'\s\s+', ' ', words_no_Punc)
    # words_no_newline = re.sub(r' newline ', r' <NEWLINE> ', words_no_double_blank).split(" ")
    # s = " ".join(words_no_newline[:maxlen]).strip()
    file3.write(test_data.strip() + "\n")

    # test_data_split = test_data.split(" ", maxsplit=1)
    # score = int(test_data_split[0].split("__label__", maxsplit=1)[1])
    # if score >= 5:
    #     file5.write("__label__pos " + test_data_split[1].strip() + "\n")
    # else:
    #     file5.write("__label__neg " + test_data_split[1].strip() + "\n")

file1.close()
file2.close()
file3.close()

