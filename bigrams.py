import nltk

def tokenize(df):
    tokens = []
    for desc in df.photo_desc:
        tokens.append(nltk.word_tokenize(desc))
    tokens = [item.lower() for l in tokens for item in l]
    return tokens

def bigrams_colloc(df):
    tokens - tokenize(df)
    finder = nltk.BigramCollocationFinder.from_words(tokens)
    bigram_measure = nltk.collocations.BigramAssocMeasures()
    return finder, bigram_measure

def bigrams_standard(df):
    tokens = tokenize(df)
    bigrams = nltk.bigrams(tokens)
    fdist = nltk.FreqDist(bigrams)
    return bigrams, fdist
