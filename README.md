# Project: Book Indexing
This project allows users to index a collection of books using NLP and ML techniques.

## Design

The project uses the NLTK and PDFMiner libraries (among others) to extract data from a Calibre library, determine keywords, and find similar books in order to classify unlabeled books.

## Pages


## Routes


## Data structures and database

Data is captured in json files on the file systems.

`title.json`:

`English_wordlist.json`

`words.txt`

`corpus_data.json`: JSON data with the following structure:
```
{"categories": ["category1", "category2", ...], 
 "freq": ["word": frequency, ...]}
 ```

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

`convert_pdf_to_txt(full_path)`: Extracts text from a PDF.

`filter_English_words(test_word_file, corpus_word_file, number_invalid_words)`: Filter a word file against a known corpus of English words.  Returns the valid words for further processing and the top n invalid words to determine how good the corpus_word_file is.  If it returns a high frequency of recognizable English words, a better corpus might be needed.  This return loop may be modified in the future to directly update the base English corpus.'''

`analyze_title(full_path, filename)`: Provides basic NLP analysis of an extracted title.  Saves the result in a title.json file.

`locate_files(extension, path_to_library)`: Finds all files with specified extension in a defined path and returns a list of tuples with paths and filenames.

When the module is run via `python extract_words.py`, a specified directory (and subdirectories) is evaluated for PDFs. Each PDF is extracted, analyzed and the results stored in a title-specific json file containing words, word frequencies and word percentages.

### text_processing.py

This module extracts keywords for each title by comparing the word frequency within a title with the word frequency in a general corpus, `corpus_data.json`. This corpus is currently generated from the Brown data, but in the future this should be supplemented with other, and more modern sources. 

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
 7. Use command `python corpus_processing.py` to create an initial corpus json file.
 8. Use command `python corpus_utilities.py` to ensure the English wordlist json file is present.

 ## Instructions

* Change `path_to_library` variable (roughly line 217) to point to a folder of PDFs.
* Use command `python extract_words.py` to build the corpus of new titles.
* Use command `python text_processing.py` to create keywords for each of the titles.
* Access the application on http://localhost:8000/ (eventually)

## Authors

* Ken Brooks, Treadwell Media Group