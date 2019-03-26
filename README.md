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

### corpus_utilities.py

### extract_words.py

### text_processing.py

## Getting started

### Prerequisites
1. [Python 2](https://www.python.org/download/releases/python-2715/) - The code uses ver 2.7.15
2. [NLTK](https://www.sqlite.org/) - Natural Language Processing Library
3. [pdfMiner](https://www.sqlalchemy.org) - Library for extracting text from PDFs.
4. [flask](http://flask.pocoo.org) - A web microframework
   for Python.

### Installing

 1. Download the latest version of Python from the link in Prerequisites.
 2. Install NLTK via `pip install nltk`.
 3. Install the Brown corpus via the python shell.
 4. Install pdfMinder
 5. Clone this repository.
 6. Use command `python corpus_processing.py` to create the corpus json file.

 ## Instructions

* Use command `python xxx.py` to run the application...
* Access the application on http://localhost:8000/ (eventually)

## Authors

* Ken Brooks, Treadwell Media Group