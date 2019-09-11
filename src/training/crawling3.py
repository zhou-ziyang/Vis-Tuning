import csv
from bs4 import BeautifulSoup
import lxml
import requests
import re

movies = -1
number_per_rating = 10000
number_per_movie_rating = 4
processed = 1144
start = processed + 1

files_ID = []
files_Review = []
review_count = [4444, 4243, 4342, 4447, 4519, 4547, 4549, 4545, 4488, 4551]
review_sum = 44230
train_set = []
dev_set = []
test_set = []

for i in range(10):
    files_ID.append(open("IMDB_Crawled/data3/imdb_id_" + str(i + 1) + ".txt", "a"))
    files_Review.append(open("IMDB_Crawled/data3/imdb_review_" + str(i + 1) + ".txt", "a"))
    # review_count.append(0)

with open("movie_metadata.csv", "r", encoding="utf-8") as f:
    f_csv = csv.DictReader(f)
    count = processed
    rows = [row['movie_imdb_link'] for row in f_csv][start:] if movies == -1 \
        else [row['movie_imdb_link'] for row in f_csv][start:start + movies]
    for url in rows:
        movie_id = re.search('\\w*(?=\\/\\?)', url)[0]
        count += 1
        print("Movie " + str(count) + ": " + movie_id)
        for i in range(10):
            if review_count[i] < number_per_rating:
                rating = i + 1
                review_url = url.replace("?ref_=fn_tt_tt_1", "reviews?sort=helpfulnessScore&dir=desc&ratingFilter=" +
                                         str(rating))
                response = requests.get(review_url)
                page_soup = BeautifulSoup(response.text, 'lxml')
                review_list = page_soup.find_all("div", class_="lister-item-content")[:number_per_movie_rating]
                for review_box in review_list:
                    review = review_box.find("div", class_=["text", "show-more__control"])
                    # review_text = re.search(r'(?<=control">)[\S\s]*(?=<\/div>)', str(review))[0]
                    # review_string = review_text.replace("<br/><br/>", "<br/>").replace("<br/>", " <NEWLINE> ")
                    review_text = str(review)
                    review_no_head = re.sub(r'<[\S\s]*control">', '', review_text)
                    review_no_tail = re.sub(r'<\/div>', '', review_no_head)
                    review_strip = re.sub(r'(<br/>)+', ' <NEWLINE> ', review_no_tail)
                    review_string = re.sub(r'[\s]+', ' ', review_strip)
                    # print(review_string)
                    files_ID[i].write(movie_id + "\n")
                    files_Review[i].write("__label__" + str(rating) + " " + review_string + "\n")
                    review_count[i] += 1
                    review_sum += 1
                    if review_count[i] >= number_per_rating:
                        break
        print(review_count)
        print("Sum: " + str(review_sum))
        if review_sum >= number_per_rating * 10:
            break

for i in range(10):
    files_ID[i].close()
    files_Review[i].close()
