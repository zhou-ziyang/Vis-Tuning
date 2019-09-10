import codecs
import os

maxlen = 400

data_path = "/Users/zhouziyang/Documents/LMU/Studium/Informatik/Bachelorarbeit/aclImdb"  # 文件夹目录


def load_data(data_path, new_files, set_type, asp):
    path = "/".join([data_path, set_type, asp])
    files = os.listdir(path)
    print(path)
    for file in files:  # 遍历文件夹
        new_path = path + "/" + file
        if not os.path.isdir(new_path):  # 判断是否是文件夹，不是文件夹才打开
            with open(new_path, 'r') as f_in:
                rating = str(file).split(sep="_")[1].split(sep=".")[0]
                sentence = " ".join([line.strip() for line in f_in])
                # sentence = [line.strip() for line in f_in][0]

                label_rating = "__label__" + rating
                content_rating = label_rating + " <START> " + sentence + "\n"
                new_files[0].write(content_rating)

                label_asp = "__label__" + asp
                content_aspect = label_asp + " <START> " + sentence + "\n"
                new_files[1].write(content_aspect)

                content_both = label_asp + " " + label_rating + " <START> " + sentence + "\n"
                new_files[2].write(content_both)


for set_type in ["train", "test"]:
    file_rating = open("IMDB_Rating_Data/imdb_rating." + set_type, "w")
    file_aspect = open("IMDB_Rating_Data/imdb_aspect." + set_type, "w")
    file_both = open("IMDB_Rating_Data/imdb_both." + set_type, "w")
    new_files = [file_rating, file_aspect, file_both]
    for asp in ["neg", "pos"]:
        load_data(data_path, new_files, set_type, asp)
    file_rating.close()
    file_aspect.close()
    file_both.close()
