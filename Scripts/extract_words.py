from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import nltk
from nltk.corpus import stopwords

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'  # utf-8
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

def whatisthis(s):
    if isinstance(s, str):
        print "acii"
    elif isinstance(s, unicode):
        print "unicode"
    else:
        print "not a string"


#path = "/Users/kbrooks/Documents/Book indexing project/Test Library/Allen B. Downey/Think Complexity (11)/Think Complexity - Allen B. Downey.pdf"
path = "/Users/kbrooks/Documents/Book indexing project/Test Library/Cosma Shalizi/split, apply, combine with plyr (1)/split, apply, combine with plyr - Cosma Shalizi.pdf"

print "Starting PDF extraction..."
book = convert_pdf_to_txt(path)

print "Starting tokenizing..."

# 1. for each document of the corpus:
# - tokenize
tokens = nltk.wordpunct_tokenize(book)
text = nltk.Text(tokens)

# - toLowerCase, trim
words = [w.lower() for w in text]

# Test for unicode

#unicode_test = [whatisthis(w) for w in words]
#print unicode_test

#words = [w.encode('utf-16')  for w in words]

# - replace \ with space

words = [w.replace("\\", " ") for w in words]  # I think the problem is that I'm trying to replace unicode

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

print "Removing stopwords..."
# 5. remove stop words
# //there are many criteria here, but the main ones are:
# - if it is a unigram, remove it if it is in the list of stopwords
# - if it is a bi-gram or above, remove it IF some of its token belongs to the list of stopwords

stopwords = set(stopwords.words('english'))
#stopword_test = [whatisthis(w) for w in stopwords]

#print stopword_test

newwords = [w for w in words if w not in stopwords]

# 6. keep only the n most frequent n-grams (n depends on the size of your corpus and your goals)

# 7. remove redundant n-grams
# // eg: if a = "University of" and b= "University of Amsterdam" are both in the list of most frequent n-grams, 
# //remove a because it is contained in b, and because it is not n times more frequent than b (I found that a n of 2 or 3 works fine). 

# 8. count the occurrences of each remaining n-gram in each document

# 9. proceed with the rest of the text analysis!

# As you see, I found that the stopwords removal should arrive quite late in the steps, and in any case after the detection of n-grams. 
# Also, I improved a lot my results by fine tuning my list of stopwords, and by creating several lists of stopwords. You should not 
# hesitate to use a long list I believe, in my case I have excellent results with about 5500 stopwords. This is a topic in itself, 
# we should discuss it some time!


vocab = sorted(set(newwords))

print vocab