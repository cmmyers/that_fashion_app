def collect_similar(word, model, n_output):

    #using a word2vec model find n words most similar to the given words
    #and return as a list [include the original word in the list]


#     with open(model_path) as f:
#         model = pickle.load(f)

    most_sim = model.most_similar(word, topn=n_output)
    most_sim_list = [item[0] for item in most_sim]
    most_sim_list.append(word)

    return most_sim_list


def make_bigrams(text, root_word, stopwords=["a", "the"], root_word_first = False):
    '''
    how should we expect the text to arrive? list of words? list of lists of words?
    pandas series?
    root_word_first --> figure out whether to create a bigram with the root word
    first or second
    currently this only works for root word as second word

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

        return new_text

    except IndexError:
        return [""]

def bigrams_for_similar_garments(word, text_series, model, num_sim=10):
    root_words = collect_similar(word, model, num_sim)
    new_texts = []
    for text in text_series:
        for word in root_words:
            text = make_bigrams(text, word)
        new_texts.append(text)
    return new_texts

def bigrams_for_all_garments(text_series, model, num_sim=10):
    basic_garments = ["dress", "pants", "shirt", "shoes"]
    for garment in basic_garments:
        text_series = bigrams_for_similar_garments(garment, text_series, model, num_sim)

    return text_series
