import os
import json

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from nltk.corpus import stopwords as corpus_stopwords
from nltk.corpus import words as corpus_words
import nltk



def convert_pdf_to_txt(full_path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(full_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def filter_English_words(test_word_file, corpus_word_file, number_invalid_words):
    '''Filter a word file against a known corpus of English words.  Returns the valid 
    words for further processing and the top n invalid words to 
    determine how good the corpus_word_file is.  If it returns a high frequency of 
    recognizable English words, a better corpus might be needed.  This return loop 
    may be modified in the future to directly update the base English corpus.'''

    English_words = [w.lower() for w in corpus_word_file]  # make all of the words lower case

    English_words = set(English_words)  # eliminate duplicates and turn them into a set for faster processing

    valid_words =  [w for w in test_word_file if w in English_words]

    invalid_words =  [w for w in test_word_file if w not in English_words]  

    invalid_text_freq = nltk.FreqDist(invalid_words)  # calculate frequencies
        
    n_invalid_words = invalid_text_freq.most_common(number_invalid_words)

    n_invalid_words = [word for word, count in n_invalid_words]

    return valid_words, n_invalid_words

def analyze_title(full_path, filename):
    '''Provides basic NLP analysis of an extracted title.  Saves the result in a title.json file'''
    try:
        title_dict = json.load(open('data/' + filename + '.json'))
        print "title_dict imported"
    except IOError:  # 
        print "No existing title dictionary, creating empty dictionary"
        title_dict = {}

    title_dict["title"] = filename


    print "Starting extraction..."


    if "extract" in title_dict:
        book = title_dict["extract"]
    else:
        book = convert_pdf_to_txt(full_path)
        title_dict["extract"] = book

    #print title_dict

    print "Starting tokenization..."
    # 1. for each document of the corpus:
    # - tokenize
    tokens = nltk.wordpunct_tokenize(book)
    text = nltk.Text(tokens)

    # - toLowerCase, trim
    words = [w.lower() for w in text]           # lower case
    words = [w for w in words if len(w)<=20]    # excessively long words
    words = [w for w in words if len(w)>2]      # excessively short words
    # words = [w for w in words if w.isalpha()] # numbers and punctuation

    # - remove non-English words (until I have a bettr corpus)

    print "Starting word filtering..."

    English_wordlist= json.load(open('../data/' + "English_wordlist" + '.json'))
    words, invalid_words = filter_English_words(words, English_wordlist, 10)

    # - delete all non printable characters with a regex
    # - trim again
    # - delete multiple white spaces
    # - 1.1. Looping on each token of this document:
    # -  lemmatization by replacing plurals by singulars using simple heuristics 
    # (it takes me just 15 lines of code)
    # - append the resulting string to the global string containing all documents.

    # 2. extract n-grams (unigrams, bigrams, trigrams, 4-grams) of the global string and count 
    # their frequency

    # 3. remove n-grams with length < 3

    # 4. remove n-grams which appear just once or twice (unjustified but reasonable absolute cut-off, help to clean a lot!)

    # 5. remove stop words
    print "Removing stopwords..."
    # //there are many criteria here, but the main ones are:
    # - if it is a unigram, remove it if it is in the list of stopwords
    # - if it is a bi-gram or above, remove it IF some of its token belongs to the list of stopwords

    stopwords = set(corpus_stopwords.words('english')) ## O(1) instead of O(n)

    print "stopword file created"
    # def word_filter(word):
    #     return (word.isalpha() and          # kill words with numbers
    #             len(word) <= 20 and         # kill excessively long words
    #             word not in stopwords)      # kill English stopwords

    words = [w for w in words if w not in stopwords]

    # 6. keep only the n most frequent n-grams (n depends on the size of your corpus and your goals)

    # 7. remove redundant n-grams
    # // eg: if a = "University of" and b= "University of Amsterdam" are both in the list of most frequent n-grams, 
    # //remove a because it is contained in b, and because it is not n times more frequent than b (I found that a n of 2 or 3 works fine). 

    # 8. count the occurrences of each remaining n-gram in each document

    # 9. proceed with the rest of the text analysis!

    # As you see, I found that the stopwords removal should arrive quite late in the steps, and in any case after the detection 
    # of n-grams. Also, I improved a lot my results by fine tuning my list of stopwords, and by creating several lists of stopwords. 
    # You should not hesitate to use a long list I believe, in my case I have excellent results with about 5500 stopwords. This is a 
    # topic in itself, we should discuss it some time!

    title_dict["words"] = words

    # capture title statistics
    print "Calculating title statistics:\n"
    text_freq = nltk.FreqDist(words)
    text_size = len(words)
    text_pcnt = {word:text_freq[word] / float(text_size) for word in text_freq.keys()}
    title_dict["freq"] = text_freq
    text_vocab = sorted(set(words))
    title_dict["vocab"] = text_vocab
    title_dict["percent"] = text_pcnt

    tenMostCommon= text_freq.most_common(10)
    print "Number of words:", text_size
    print "Unique words", len(text_vocab), "\n"
    for w in tenMostCommon: print w

    # data
    with open('../data/' + filename + '.json', 'w') as outfile:
        json.dump(title_dict, outfile, 
            sort_keys = True, 
            indent = 4,
            # ensure_ascii=False,
            )

def locate_files(extension, path_to_library):
    '''Finds all files with specified extension in a defined path 
    and returns a list of tuples with paths and filenames'''

    search_list = []

    for root, dirs, files in os.walk(path_to_library):
        for file in files:
            if file.endswith(".pdf"):
                print root
                print file
                print(os.path.join(root, file))
                search_list.append((root, file))
    return search_list

# from collections import Counter
# c = Counter(words)

# print c
# import ipdb; ipdb.set_trace()

if __name__ == "__main__":

    # Test for filter_English_words
    test_word_file = [u'learning', u'decision', u'tree', u'based', u'computational']
    corpus_word_file = [u'this', u'is', u'a', u'cat', u'computational']
    valid_words, invalid_words = filter_English_words(test_word_file, corpus_word_file, 10)
    assert valid_words == [u'computational']
    assert invalid_words == [u'based', u'decision', u'tree', u'learning']

    #working_dir = os.path.dirname(os.path.abspath(__file__))

    #library_list = [("../Test Library/Allen B. Downey/Think Complexity (11)", "Think Complexity - Allen B. Downey.pdf"),
    #               ("../Test Library/Pierre Geurts/Supervised Larning with Decision Tree-based methods in Computational and Systems Biology (4)/", "Supervised Larning with Decision Tree-base - Pierre Geurts.pdf")]
                  
    # library_list = [('/Users/kbrooks/Documents/Book indexing project/Test Library/Abhijat Vichare/Theory of Computation Lecture Notes, August 2005 (9)', 'Theory of Computation Lecture Notes, Augus - Abhijat Vichare.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Allen B. Downey/Think Complexity (11)', 'Think Complexity - Allen B. Downey.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Allen B. Downey/Think OS_ A Brief Introduction to Operating Systems (12)', 'Think OS_ A Brief Introduction to Operatin - Allen B. Downey.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Carol Zander/Turing Machine Examples (14)', 'Turing Machine Examples - Carol Zander.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Charles Brubaker/Supplemental Linear Programming and Duality problems (5)', 'Supplemental Linear Programming and Dualit - Charles Brubaker.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Charles Brubaker/Supplemental Maximum Flow Exercises (6)', 'Supplemental Maximum Flow Exercises - Charles Brubaker.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Cosma Shalizi/split, apply, combine with plyr (1)', 'split, apply, combine with plyr - Cosma Shalizi.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Ding-Zhu Du/Theory of Computational Complexity, 2e (10)', 'Theory of Computational Complexity, 2e - Ding-Zhu Du.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Donald Knuth/The Tex Book (7)', 'The Tex Book - Donald Knuth.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Harold Abelson/Structure and Interpretation of Computer Programs (2)', 'Structure and Interpretation of Computer P - Harold Abelson.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Harold Abelson/Structure and Interpretation of Computer Programs, 2e (3)', 'Structure and Interpretation of Computer P - Harold Abelson.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Mitsunori Ogihara/Theory and Applications of Models of Computation_ 8th Annual Conference, TAMC 2011, Tokyo, Japan (8)', 'Theory and Applications of Models of Compu - Mitsunori Ogihara.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Pierre Geurts/Supervised Larning with Decision Tree-based methods in Computational and Systems Biology (4)', 'Supervised Larning with Decision Tree-base - Pierre Geurts.pdf'), 
    #                 ('/Users/kbrooks/Documents/Book indexing project/Test Library/Roger Zelazny/Trumps of Doom (13)', 'Trumps of Doom - Roger Zelazny.pdf')]

    path_to_library = "/Users/kbrooks/Dropbox/Projects/BookIndexing/Test Library"
    extension = ".pdf"

    library_list = locate_files(extension,path_to_library)

    error_log = []

    for path, filename in library_list:
        
        full_path = os.path.join(path, filename)
        print full_path
        try:
            analyze_title(full_path, filename)
        except Exception as ex:
            error_log.append((str(ex), path, filename))

    for log in error_log:
        print log[0], log[2]

