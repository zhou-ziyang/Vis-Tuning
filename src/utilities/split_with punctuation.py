import codecs
import re


def split_with_punctuation(sentence):
    s = re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r'<BREAK>', sentence)
    return(s)


# review = 'The story of the Zodiac could have been interesting but this movie proved to be a two hour and forty minute ' \
#          'bore-fest. Most of the movie is spent on the investigation as scene after scene piles on pieces of evidence ' \
#          'for the characters to ponder. The movie tries (and fails) to show you how the investigation adversely ' \
#          'affected the lives of a reporter (played by Robert Downey Jr), a homicide inspector (played by Mark ' \
#          'Ruffalo), and a cartoonist (played by Jake Gyllenhaal) hence the poster\'s tag line "There\'s more than one ' \
#          'way to lose your life to a killer.\" <NEWLINE> The strategy of the movie is this: To show how frustrating ' \
#          'and tiresome a murder investigation can be, the movie wants to put you through a frustrating and tiresome ' \
#          'experience. To make us feel the way the characters spent long wasted hours sifting through the minutiae of ' \
#          'the case in the vain effort to arrest a suspect, the movie puts you through a long 160 minutes of minutiae ' \
#          'for you to sift through. The movie worked on me as intended I was maddeningly frustrated and extremely ' \
#          'tired. This is great story-telling? Nope, I\'m not buying that pretentious load of baggage. <NEWLINE> How ' \
#          'did the Zodiac affect the main characters? I wouldn\'t know. The movie never tries to understand them ' \
#          'emotionally or psychologically. The script doesn\'t give them much to do except sift minutiae and the ' \
#          'acting can\'t seem to rise above the ponderous bleakness stretched across the whole production. <NEWLINE> ' \
#          'Zodiac is a waste of your time. Wait and see it on late night cable when you need to catch up on some sleep. '


file = codecs.open("../static/data/gamedata.txt", "w")

with codecs.open('../static/data/reviews_for_game.csv', 'r') as f_in:
    for line in f_in:
        file.write(split_with_punctuation(line.strip()) + "\n")

file.close()
