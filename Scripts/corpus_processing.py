import nltk
from nltk.corpus import brown
import json

def prep_corpus():
    '''Calculates the percent frequency of words in a the Brown corpus and dumps them
    to a json file.'''
    corpus_data = {}
    categories = ['adventure', 'belles_lettres', 'fiction', 'government', 'hobbies',
        'humor', 'learned', 'mystery', 'religion', 'romance', 'science_fiction']
    categories = ['adventure']
    corpus_data['categories'] = categories
    corpus_text = brown.words(categories = categories)
    corpus_size = len(corpus_text)
    corpus_dist = nltk.FreqDist(w.lower() for w in corpus_text)
    corpus_data['freq'] = corpus_dist
    #corpus_pcnt = {word:corpus_dist[word] / float(corpus_size) for word in corpus_dist.keys()}
    with open('../data/corpus_data.json', 'w') as outfile:
        json.dump(corpus_data, outfile, 
            sort_keys = True, 
            indent = 4,
            # ensure_ascii=False,
            )

if __name__ == "__main__":

    prep_corpus()