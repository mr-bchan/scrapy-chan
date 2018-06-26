import nltk
import re
from nltk.tokenize import RegexpTokenizer


def tokenize(documents):
    # Tokenize documents
    tokens = []
    with open('../nlp/stop_words.txt', 'r') as file:
        stopwords = file.read().split()

    for idx, p in enumerate(documents):
        data_tokens = RegexpTokenizer(r'#?\w+').tokenize(p)
        filtered_tokens = [unicode(w, errors='ignore').lower() for w in data_tokens
                           if w.lower() not in stopwords  # filter stop words
                           and not bool(re.search(r'\d', w))  # words with numbers
                           and len(w) > 2]  # filter short words (1-2 letter words)
        tokens = tokens + filtered_tokens

    return tokens