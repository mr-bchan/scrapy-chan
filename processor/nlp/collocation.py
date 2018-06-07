import nltk
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

import re

from nltk.tokenize import RegexpTokenizer


class Collocation():

    def __init__(self, db_helper, filter_ngram=5, ngram_window_size=15):

        # Get all posts
        posts = db_helper.get_posts(['title','summary', 'description'], '*')
        posts = ["{} {} {}".format(x[0], x[1], x[2]) for x in posts]

        # Tokenize documents
        tokens = []
        with open('../nlp/stop_words.txt','r') as file:
            stopwords = file.read().split()
        stopwords = stopwords + ['https','www', 'http', 'bit', 'ly', 'goo', 'gl']

        for idx,p in enumerate(posts[0:20000]):
            data_tokens = RegexpTokenizer(r'#?\w+').tokenize(p)
            filtered_tokens = [unicode(w, errors='ignore').lower() for w in data_tokens
                               if w.lower() not in stopwords           # filter stop words
                               and not bool(re.search(r'\d', w))       # words with numbers
                               and len(w) > 1]                         # filter short words (1-2 letter words)

            tokens = tokens + filtered_tokens
            print(idx)

            print(p)
            print(filtered_tokens)
            print('--------------')


        # Find all bigrams using BigramCollocationFinder
        self.finder = BigramCollocationFinder.from_words(tokens, ngram_window_size)
        self.finder.apply_freq_filter(filter_ngram)

        self.scores = self.finder.score_ngrams(bigram_measures.pmi)[::1]


    def get_links(self, term):
        terms = term.split(' ')


        #{id,group,label,level}
        nodes = []
        node_ids = []

        #{source,target,strength}
        links = []

        # # Append root node
        nodes.append({
            "id": "_root_",
            "group": 1,
            "label": "",
            "level": 2
        })

        for t in terms:
            bigrams = [x for x in self.scores if t in x[0] and x[1] > 0][:20]

            nodes.append({
                "id": t,
                "group": 1,
                "label": t,
                "level": 1
            })

            links.append({
                "target": "_root_",
                "source": t,
                "strength": 0})

            # Add to unique node ids
            node_ids.append(t)
            for pair in bigrams:
                print(pair)

                # Add pairs to node list if nodes not yet stored and not in terms list
                if pair[0][0] not in node_ids and pair[0][0] not in terms:
                    nodes.append({
                        "id": pair[0][0],
                        "group": 0,
                        "label": pair[0][0],
                        "level": 0
                    })
                    node_ids.append(pair[0][0])

                if pair[0][1] not in node_ids and pair[0][1] not in terms:
                    nodes.append({
                        "id": pair[0][1],
                        "group": 0,
                        "label": pair[0][1],
                        "level": 0
                    })
                    node_ids.append(pair[0][1])

                links.append({
                    "target": pair[0][0],
                    "source": pair[0][1],
                    "strength": round(pair[1],2)})

        print(nodes)
        print(links)
        # Process nodes:
        return {"nodes": nodes,
                "links": links}
