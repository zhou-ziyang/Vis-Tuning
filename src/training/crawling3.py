import csv
from bs4 import BeautifulSoup
import lxml
import requests
import re

movies = 2
number_of_reviews = 100000
files_ID = []
files_Review = []
review_count = []
review_sum = 0
train_set = []
dev_set = []
test_set = []
for i in range(10):
    files_ID.append(open("IMDB_Crawled/data2/imdb_id_" + str(i + 1) + ".txt", "w"))
    files_Review.append(open("IMDB_Crawled/data2/imdb_review" + str(i + 1) + ".txt", "w"))
    review_count.append(0)

with open("movie_metadata.csv", "r", encoding="utf-8") as f:
    f_csv = csv.DictReader(f)
    count = 0
    rows = [row['movie_imdb_link'] for row in f_csv] if movies == -1 \
        else [row['movie_imdb_link'] for row in f_csv][:movies]
    for url in rows:
        movie_id = re.search('\\w*(?=\\/\\?)', url)[0]
        count += 1
        print("Movie " + str(count) + ": " + movie_id)
        for i in range(10):
            rating = i + 1
            review_url = url.replace("?ref_=fn_tt_tt_1", "reviews?sort=helpfulnessScore&dir=desc&ratingFilter=" +
                                     str(rating))
            response = requests.get(review_url)
            page_soup = BeautifulSoup(response.text, 'lxml')
            review_list = page_soup.find_all("div", class_="lister-item-content")
            for review_box in review_list:
                review = review_box.find("div", class_=["text", "show-more__control"]).text
                files_ID[i].write(movie_id + "\n")
                files_Review[i].write("__label__" + str(rating) + " " + review + "\n")
                review_count[i] += 1
                review_sum += 1
                if review_sum >= number_of_reviews:
                    break
            print(review_count)
            print("Sum: " + str(review_sum))

for i in range(10):
    files_ID[i].close()
    files_Review[i].close()
