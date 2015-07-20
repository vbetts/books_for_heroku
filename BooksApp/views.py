from django.shortcuts import render
import re
import operator
import os
from . import find_common_sentences

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Book file paths
DRACULA = os.path.join(BASE_DIR, 'BooksApp/book_files/dracula.txt')
ALICE = os.path.join(BASE_DIR, 'BooksApp/book_files/aliceinwonderland.txt')
TWO_CITIES = os.path.join(BASE_DIR, 'BooksApp/book_files/ataletwocities.txt')
MOBY_DICK = os.path.join(BASE_DIR, 'BooksApp/book_files/mobydick.txt')
PRIDE_PREJUDICE = os.path.join(BASE_DIR, 'BooksApp/book_files/prideprejudice.txt')

# Misc other file paths
STOPWORDS = os.path.join(BASE_DIR, 'BooksApp/word_exclusions/stopwords.txt')
F_PRONOUNS = os.path.join(BASE_DIR, 'BooksApp/word_exclusions/female_pronouns.txt')
M_PRONOUNS = os.path.join(BASE_DIR, 'BooksApp/word_exclusions/male_pronouns.txt')
ALL_PRONOUNS = os.path.join(BASE_DIR, 'BooksApp/word_exclusions/maleandfemale.txt')
N_PRONOUNS = os.path.join(BASE_DIR, 'BooksApp/word_exclusions/neutral_pronouns.txt')
CSV_PREFIX = os.path.join(BASE_DIR, 'BooksApp/static/BooksApp/csv')
NO_STOPWORDS = os.path.join(BASE_DIR, 'BooksApp/word_exclusions/none.txt')


def read_book(filename):
    words = []
    # Matches non-alphanumeric characters.
    ignore_regex = re.compile('[^0-9a-zA-Z]+')
    with open(filename, 'r') as f:
        for line in f:
            # Replace non-alphanumeric characters with spaces and lower case the line.
            normalized_line = ignore_regex.sub(' ', line.lower())
            for word in normalized_line.split():
                words.append(word)
    return words


# Create list of 'special words'
def special_word_list(list_file):
    return set(read_book(list_file))


# Take book file path and list of stopwords
# Return list of all words in book (excluding stopwords) and the number of times they appear
# ordered by frequency
def order_wordcount(book_file, stopwords):
    words = []
    exclude = special_word_list(stopwords)
    regex = re.compile('[^a-zA-Z]')

    with open(book_file, 'r') as f:
        for line in f:
            for word in line.split():
                if regex.sub('', word.lower()) not in exclude:
                    words.append(regex.sub('', word.lower()))

    counts = dict()

    for w in words:
        if w in counts.keys():
            counts[w] += 1
        else:
            counts[w] = 1

    counts_sorted = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)

    return counts_sorted


# Take a text file of specified words and book file path
# Return  the number of occurrences of each word in the book
def count_specific_words(book_file, word_list):
    words = []
    include = special_word_list(word_list)
    regex = re.compile('[^a-zA-Z]')

    with open(book_file, 'r') as f:
        for line in f:
            for word in line.split():
                if regex.sub('', word.lower()) in include:
                    words.append(regex.sub('', word.lower()))

    counts = dict()

    for w in words:
        if w in counts.keys():
            counts[w] += 1
        else:
            counts[w] = 1

    counts_sorted = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)

    return counts_sorted


# Take book file path
# Return the first sentence (from start of text until first period) in string format
def first_sentence(book_file):
    sentence_rough = []
    sentence_characters = []
    sentence_start = "-----"
    sentence_end = "."

    with open(book_file, 'r') as f:
        # Start reading the file at the annotated trigger (-----)
        for line in f:
            if line.strip() == sentence_start:
                break
        # Add lines to the array until line containing a period is reached
        for line in f:
            sentence_rough.append(line.replace('\n', ' '))
            if sentence_end in line:
                break

    # Add the extracted characters to a new array only until the period is reached
    for line in sentence_rough:
        for character in line:
            sentence_characters.append(character)
            if character == sentence_end:
                break

    # Join the cleaned-up array of characters into a string
    sentence_final = ''.join(sentence_characters)
    return sentence_final

def count_frequencies(word_array):
    count_freq = 0
    for item in word_array:
        count_freq += item[1]
    return count_freq

def convert_wordcount(wordcount):
    wordlist = []
    for word in wordcount:
        wordlist.append(word[0])
    return wordlist


def index(request):

    ordered_alice = convert_wordcount(order_wordcount(ALICE, STOPWORDS))
    ordered_dracula = convert_wordcount(order_wordcount(DRACULA, STOPWORDS))
    ordered_moby = convert_wordcount(order_wordcount(MOBY_DICK, STOPWORDS))
    ordered_pp = convert_wordcount(order_wordcount(PRIDE_PREJUDICE, STOPWORDS))
    ordered_two_cities = convert_wordcount(order_wordcount(TWO_CITIES, STOPWORDS))

    f_count_moby_dick = count_frequencies(count_specific_words(MOBY_DICK, F_PRONOUNS))
    m_count_moby_dick = count_frequencies(count_specific_words(MOBY_DICK, M_PRONOUNS))

    f_count_alice = count_frequencies(count_specific_words(ALICE, F_PRONOUNS))
    m_count_alice = count_frequencies(count_specific_words(ALICE, M_PRONOUNS))

    he_counts = []
    him_counts = []
    his_counts = []
    himself_counts = []
    she_counts = []
    her_counts = []
    hers_counts = []
    herself_counts = []

    alice_pronouns = dict(count_specific_words(ALICE, ALL_PRONOUNS))
    twocities_pronouns = dict(count_specific_words(TWO_CITIES, ALL_PRONOUNS))
    dracula_pronouns = dict(count_specific_words(DRACULA, ALL_PRONOUNS))
    moby_pronouns = dict(count_specific_words(MOBY_DICK, ALL_PRONOUNS))
    pp_pronouns = dict(count_specific_words(PRIDE_PREJUDICE, ALL_PRONOUNS))

    pronouns_by_ordered_book = [alice_pronouns,
                                dracula_pronouns,
                                moby_pronouns,
                                pp_pronouns,
                                twocities_pronouns]

    for book in pronouns_by_ordered_book:
        total = sum(book.values())
        he_counts.append(round(100 * book.get("he", 0)/total, 2))
        him_counts.append(round(100 * book.get("him", 0)/total, 2))
        his_counts.append(round(100 * book.get("his", 0)/total, 2))
        himself_counts.append(round(100 * book.get("himself", 0)/total, 2))
        she_counts.append(round(100 * book.get("she", 0)/total, 2))
        her_counts.append(round(100 * book.get("her", 0)/total, 2))
        hers_counts.append(round(100 * book.get("hers", 0)/total, 2))
        herself_counts.append(round(100 * book.get("herself", 0)/total, 2))

    opening_line_alice = first_sentence(ALICE)
    opening_line_dracula = first_sentence(DRACULA)
    opening_line_moby = first_sentence(MOBY_DICK)
    opening_line_pp = first_sentence(PRIDE_PREJUDICE)
    opening_line_two_cities = first_sentence(TWO_CITIES)

    common_sequences_ad = find_common_sentences.find_longest_common_sequences(read_book(ALICE),
                                                                           read_book(DRACULA))
    common_sequences_pp_md = find_common_sentences.find_longest_common_sequences(read_book(PRIDE_PREJUDICE),
                                                                                 read_book(MOBY_DICK))
    common_sequences_a_tt = find_common_sentences.find_longest_common_sequences(read_book(ALICE),
                                                                                read_book(TWO_CITIES))


    return render(request, 'BooksApp/index.html', {'opening_line_alice': opening_line_alice,
                                                   'opening_line_dracula': opening_line_dracula,
                                                   'opening_line_moby': opening_line_moby,
                                                   'opening_line_pp': opening_line_pp ,
                                                   'opening_line_two_cities': opening_line_two_cities,
                                                   'ordered_dracula': ordered_dracula[0:9],
                                                   'ordered_moby': ordered_moby[0:9],
                                                   'ordered_pp': ordered_pp[0:9],
                                                   'ordered_alice': ordered_alice[0:9],
                                                   'ordered_two_cities': ordered_two_cities[0:9],
                                                   'f_count_moby_dick': f_count_moby_dick,
                                                   'm_count_moby_dick': m_count_moby_dick,
                                                   'f_count_alice': f_count_alice,
                                                   'm_count_alice': m_count_alice,
                                                   'he_counts': he_counts,
                                                   'him_counts': him_counts,
                                                   'his_counts': his_counts,
                                                   'himself_counts': himself_counts,
                                                   'she_counts': she_counts,
                                                   'her_counts': her_counts,
                                                   'hers_counts': hers_counts,
                                                   'herself_counts': herself_counts,
                                                   'common_seq_ad': common_sequences_ad,
                                                   'common_seq_pp_md': common_sequences_pp_md,
                                                   'common_seq_a_tt': common_sequences_a_tt})
