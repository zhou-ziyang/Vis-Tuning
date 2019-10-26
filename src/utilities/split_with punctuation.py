import codecs
import re


def split_with_punctuation(sentence):
    s = re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r'<BREAK>', sentence)
    return(s)


file = codecs.open("../static/data/gamedata.txt", "w")

with codecs.open('../static/data/reviews_for_game.txt', 'r') as f_in:
    for line in f_in:
        file.write(split_with_punctuation(line.strip()) + "\n")

file.close()
