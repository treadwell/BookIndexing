import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import nltk
from nltk.corpus import stopwords
import json

working_dir = os.path.dirname(os.path.abspath(__file__))
#title_path = "../Test Library/Allen B. Downey/Think Complexity (11)/"
title_path = "../Test Library/Pierre Geurts/Supervised Larning with Decision Tree-based methods in Computational and Systems Biology (4)/"

#filename = "Think Complexity - Allen B. Downey.pdf"
filename = "Supervised Larning with Decision Tree-base - Pierre Geurts.pdf"
path = os.path.join(working_dir, title_path, filename)

# files = []
# for f in os.listdir(working_dir):
#     if f.endswith(".pdf"):
#         files.append(f)


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
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

try:
    title_dict = json.load(open('../data/file_data.json'))
    print "title_dict imported"
except IOError:  # 
    print "No existing title dictionary, creating empty dictionary"
    title_dict = {}

title_dict["title"] = filename


print "Starting extraction..."


if "extract" in title_dict:
    book = title_dict["extract"]
else:
    book = convert_pdf_to_txt(path)
    title_dict["extract"] = book

#print title_dict

print "Starting tokenization..."
# 1. for each document of the corpus:
# - tokenize
tokens = nltk.wordpunct_tokenize(book)
text = nltk.Text(tokens)

# - toLowerCase, trim
words = [w.lower() for w in text]

# - remove words with numbers

words = [w for w in words if w.isalpha()]

# - remove excessively long words

words = [w for w in words if len(w)<=20]

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

stopwords = set(stopwords.words('english')) ## O(1) instead of O(n)

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
title_dict["freq"] = text_freq
text_vocab = sorted(set(words))
title_dict["vocab"] = text_vocab

tenMostCommon= text_freq.most_common(10)
print "Number of words:", len(words)
print "Unique words", len(text_vocab), "\n"
for w in tenMostCommon: print w


with open('../data/file_data.json', 'w') as outfile:
    json.dump(title_dict, outfile, 
        sort_keys = True, 
        indent = 4,
        # ensure_ascii=False,
        )


# from collections import Counter
# c = Counter(words)

# print c
# import ipdb; ipdb.set_trace()
