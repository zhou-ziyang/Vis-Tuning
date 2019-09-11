import random

train_set = []
dev_set = []
test_set = []
percentage = [0.6, 0.8]
file1 = open("IMDB_Crawled/imdb.train", "w")
file2 = open("IMDB_Crawled/imdb.dev", "w")
file3 = open("IMDB_Crawled/imdb.test", "w")

for i in range(10):
    rating = i + 1
    with open("IMDB_Crawled/data2/imdb_review_" + str(rating) + ".txt", "r") as f_in:
        review_list = [line for line in f_in]
    number = len(review_list)
    train_set += review_list[:int(number * percentage[0])]
    dev_set += review_list[int(number * percentage[0]):int(number * percentage[1])]
    test_set += review_list[int(number * percentage[1]):]

random.shuffle(train_set)
random.shuffle(dev_set)
random.shuffle(test_set)

for train_data in train_set:
    file1.write(train_data)

for dev_data in dev_set:
    file2.write(dev_data)

for test_data in test_set:
    file3.write(test_data)

file1.close()
file2.close()
file3.close()

