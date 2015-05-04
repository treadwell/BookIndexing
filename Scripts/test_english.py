from nltk.corpus import words

# - text for English words

text_words = ["built", 
        "buntine", 
        "c", 
        "california", 
        "called", 
        "cally", 
        "candidate", 
        "carolina", 
        "case", 
        "categorical", 
        "cation", 
        "celine", 
        "centered", 
        "cex", 
        "changing", 
        "chical", 
        "choice", 
        "choose", 
        "chosen", 
        "christian", 
        "clark", 
        "class", ]

print len(words.words())  # not big enough

English_words = [w.lower() for w in words.words()]

English_words = set(English_words)

text_valid =  [w for w in text_words if w in English_words]

text_invalid =  [w for w in text_words if w not in English_words]  # missing some obvious ones

print text_invalid