# Project: Book Indexing
This project allows users to index a collection of books using NLP and ML techniques.

## Design

The project uses the NLTK and PDFMiner libraries (among others) to extract data from a Calibre library, determine keywords, and find similar books in order to classify unlabeled books.

## Pages


## Routes


## Database

For now the file system is used...eventually Mongo?

## Python Scripts

### corpus_processing.py

This module calculates the percent frequency of words in a the Brown corpus and dumps them to a json file.  The corpus data will be used in later processing.

### corpus_utilities.py

This module contains two functions: 
`create_English_wordlist(textfile)`: Creates an English word list from a text file that will be used to remove unrecognized tokens in text extraction.  It provides the capability of removing words that shouldn't be in the file (removals) and addition of words that should be there (additions).

`update_English_wordlist(json_wordlist, addition_list)`: Updates an existing wordlist file with new words gathered from looking at a corpus.

When the module is run via `python corpus_utilities.py`, it shows new words that are popular in the list of titles in the data directory and whether they are shown as valid or invalid in the current `English_wordlist.json` file. These can then be manually added by updating the list of additional words, `addition_list` at the bottom of the module and running  `python corpus_utilities.py` again.



### extract_words.py

This module extracts words from books and filters them against a list of recognized English words.  It also identifies the top 'n' unrecognized words for potential inclusion in the filter.

### text_processing.py

This module extracts keywords for each title.

## Getting started

### Prerequisites
1. [Python 2](https://www.python.org/download/releases/python-2715/) - The code uses ver 2.7.15
2. [NLTK](https://www.nltk.org/) - Natural Language Processing Library
3. [pdfMiner](https://pypi.org/project/pdfminer/) - Library for extracting text from PDFs.
4. [flask](http://flask.pocoo.org) - A web microframework
   for Python.

### Installing

 1. Download the latest version of Python from the link in Prerequisites.
 2. Install NLTK via `pip install nltk`.
 3. Install the Brown corpus via the python shell.
  ```
  >>> import nltk
  >>> nltk.download('brown')
  ```
 4. Install the NLTK stopwords list via the python shell:
  ```
  >>> import nltk
  >>> nltk.download('stopwords')
  ```
 5. Install pdfMiner via `pip install pdfminer`.
 6. Clone this repository.
 7. Use command `python corpus_processing.py` to create the corpus json file.
 8. use command `python corpus_utilities.py` to ensure the English wordlist json file is present.

 ## Instructions

* Change `path_to_library` variable (roughly line 217) to point to a folder of PDFs.
* Use command `python extract_words.py` to build the corpus of new titles.
* Use command `python text_processing.py` to create keywords for each of the titles.
* Access the application on http://localhost:8000/ (eventually)

## Authors

* Ken Brooks, Treadwell Media Group