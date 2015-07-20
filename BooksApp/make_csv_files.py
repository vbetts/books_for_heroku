from BooksApp import views
import csv
import re

COUNT_PP = views.order_wordcount(views.PRIDE_PREJUDICE, views.STOPWORDS)
COUNT_DRACULA = views.order_wordcount(views.DRACULA, views.STOPWORDS)
COUNT_ALICE = views.order_wordcount(views.ALICE, views.STOPWORDS)
COUNT_TWO_CITIES = views.order_wordcount(views.TWO_CITIES, views.STOPWORDS)
COUNT_MOBY = views.order_wordcount(views.MOBY_DICK, views.STOPWORDS)

STOPWORDS_MOBY = views.count_specific_words(views.MOBY_DICK, views.STOPWORDS)
STOPWORDS_PP = views.count_specific_words(views.PRIDE_PREJUDICE, views.STOPWORDS)
STOPWORDS_DRACULA = views.count_specific_words(views.DRACULA, views.STOPWORDS)
STOPWORDS_ALICE = views.count_specific_words(views.ALICE, views.STOPWORDS)
STOPWORDS_TWO_CITIES =views.count_specific_words(views.TWO_CITIES, views.STOPWORDS)



def make_csv_file(word_array, csv_filename):
    fixed_filename = '{0}/{1}.csv'.format(views.CSV_PREFIX, csv_filename)
    with open(fixed_filename, 'w', newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerow(['word', 'frequency'])
        for item in word_array:
            write.writerow([item[0], item[1]])

make_csv_file(COUNT_PP[1:250], 'pride_prej')
make_csv_file(COUNT_ALICE[1:250], 'alice')
make_csv_file(COUNT_DRACULA[1:250], 'dracula')
make_csv_file(COUNT_TWO_CITIES[1:250], 'two_cities')
make_csv_file(COUNT_MOBY[1:250], 'moby_dick')

make_csv_file(STOPWORDS_MOBY, 'moby_stopwords')
make_csv_file(STOPWORDS_PP, 'pp_stopwords')
make_csv_file(STOPWORDS_DRACULA, 'dracula_stopwords')
make_csv_file(STOPWORDS_ALICE, 'alice_stopwords')
make_csv_file(STOPWORDS_TWO_CITIES, 'two_cities_stopwords')


