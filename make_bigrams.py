nltk_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

def manual_stopwords(boring_words, model):
    sw = []
    for word in boring_words:
        sw.append(collect_similar(word, model, 10))
    return set([item for l in man_sw for item in l])

def collect_similar(word, model, n_output):
    '''
    INPUT: word = a word
        model = a trained word2vec model (or path once I have stuff pickled)
        n_output = the number of similar words to collect
                    the root word will also be included in this list

    RETURNS: a list of words
    '''

#     with open(model_path) as f:
#         model = pickle.load(f)

    most_sim = model.most_similar(word, topn=n_output)
    most_sim_list = [item[0] for item in most_sim]
    most_sim_list.append(word)

    return most_sim_list


def make_bigrams(text, root_word, stopwords=nltk_stopwords, root_word_first = False):
    '''
    INPUT: text = a list of word tokens
        root_word = the word to be bigramified

        root_word_first --> currently this function assumes the root word
        should be the second word in the phrase. If I have time I will add
        functionality for it to be the first word (ie if my root word were
        an adjective)

    RETURNS: a modified list of word tokens
    '''

    new_text = []
    try:
        i=0
        while i < (len(text)-1):

            if text[i+1] != root_word:
                new_text.append(text[i])
                i+=1
            elif text[i] in stopwords:
                new_text.append(text[i])
                i+=1
            else:
                new_text.append('{}_{}'.format(text[i], text[i+1]))
                i+=2

        if text[-1] != root_word:
            new_text.append(text[-1])

    except IndexError:
        new_text.append('')

    return new_text



def bigrams_for_similar_garments(text_series, word, model, stopwords= nltk_stopwords, num_sim=10):
    '''
    INPUT: text_series = pandas series or list of [lists of word tokens]
        word = a root word
        model = a trained word2vec model

    RETURNS: a list of [lists of modified word tokens]
    '''
    root_words = collect_similar(word, model, num_sim)
    new_texts = []
    for text in text_series:
        for word in root_words:
            text = make_bigrams(text, word, stopwords)
        new_texts.append(text)
    return new_texts


def bigrams_for_all_garments(text_series, model, stopwords=nltk_stopwords, num_sim=10):
    basic_garments = ["dress", "pants", "shirt", "shoes"]
    for garment in basic_garments:
        text_series = bigrams_for_similar_garments(text_series, garment, model, stopwords, num_sim)

    return text_series
