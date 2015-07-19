# Finds and prints the longest common sequences of words from two text files.
# Script takes 2 filenames as arguments.

import re
import sys


# Reads a text file and returns the list of normalized words.



# Construct all consecutive word sequences of given size
# Example: size=3: { "word1 word2 word3", "word2 word3 word4", ... }
def word_sequences(words, size):
    word_sequences = set()
    for i in range(len(words) - size):
        word_sequences.add(' '.join(words[i:i+size]))
    return word_sequences


# Finds the longest sequence in common between two lists of words.
# Returns a set of strings (words joined together with spaces).
def find_longest_common_sequences(words1, words2):
    length = 2
    longest_common_sequences = set()
    while True:
        seq1 = word_sequences(words1, length)
        seq2 = word_sequences(words2, length)
        common_sequences = set.intersection(seq1, seq2)
        if not common_sequences:
            break
        length = length + 1
        longest_common_sequences = common_sequences
    return longest_common_sequences

"""
filename1 = sys.argv[1]
filename2 = sys.argv[2]

words1 = read_book(filename1)
words2 = read_book(filename2)

longest_phrases_in_common = find_longest_common_sequences(words1, words2)

print(longest_phrases_in_common)
"""
