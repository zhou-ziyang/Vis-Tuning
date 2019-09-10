import random

with open('IMDB_Crawled/IMDB_Rating_Dataset.txt', 'r') as f_in:
    count = 0
    file1 = open("IMDB_Crawled/imdb.train", "w")
    file2 = open("IMDB_Crawled/imdb.valid", "w")
    review_lists = [[], [], [], [], [], [], [], [], [], []]
    train_set = []
    test_set = []
    for line in f_in:
        # print(line)
        try:
            rating, _ = line.split(" ", maxsplit=1)
            review_lists[int(rating) - 1].append(line)
        except ValueError:
            pass

    for i in range(10):
        train_set += review_lists[i][:2000]
        test_set += review_lists[i][2000:]

    random.shuffle(train_set)
    random.shuffle(test_set)
    test_set = test_set[:20000]

    for train_data in train_set:
        file1.write("__label__" + str(train_data))

    for test_data in test_set:
        file2.write("__label__" + str(test_data))

    file1.close()
    file2.close()

