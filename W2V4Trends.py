from gensim.models import Word2Vec
from nltk.corpus import stopwords

class W2V4Trends():

    def __init__(self, model):
        self.model = model
        self.stopwords = stopwords.words('english')


    def update_stopwords(self, ask = False, colors = True):
        boring_words = ["cool", "pretty", "awesome", "fantastic", "new", "favorite"]
        if colors:
            boring_words.append(["red", "black"])
        if ask:
            more_boring_words = self.ask_for_manual_stopwords()
            boring_words.append(more_boring_words)
        man_sw = manual_stopwords(boring_words)
        all_sw = set(self.stopwords + man_sw)

        self.stopwords = all_sw

    def ask_for_manual_stopwords(self):
        cont = True
        boring_words = []
        while cont:
            new_word = raw_input("Please enter a base word or type DONE when done: ")
            if new_word.upper() == "DONE":
                cont == False
            else:
                boring_words.append(new_word)

        return boring_words

    def manual_stopwords(self, boring_words):
        sw = []
        for word in boring_words:
            sw.append(collect_similar(word, self.model, 10))

        return set([item for l in man_sw for item in l])

    def collect_similar(self, word, model, n_output):
        '''
        INPUT: word = a base vocabulary word
            model = a trained word2vec model (or path in the form Word2Vec.open('model_path'))
            n_output = the number of similar words to collect
                        the root word will also be included in this list

        RETURNS: a list of words
        '''

        most_sim = self.model.most_similar(word, topn=n_output)
        most_sim_list = [item[0] for item in most_sim]
        most_sim_list.append(word)

        return most_sim_list

    def make_bigrams(self, text, root_word, root_word_first = False):
        '''
        INPUT: text = a list of word tokens
            root_word = the word to be bigramified

            root_word_first --> currently this function assumes the root word
            should be the second word in the phrase. I would like to add
            functionality for it to be the first word (ie if my root word were
            an adjective)

        RETURNS: a modified list of word tokens
        '''

        new_text = []
        try:
            i=0
            if root_word_first:
                while i < (len(text)-1):

                    if text[i] != root_word:
                        new_text.append(text[i])
                        i += 1
                    elif text[i+1] in self.stopwords:
                        new_text.append(text[i])
                        i += 1
                    else:
                        new_text.append('{}_{}'.format(text[i], text[i+1]))
                        i += 2

                if text[-2] != root_word:
                    new_text.append(text[-1])

            else:
                while i < (len(text)-1):

                    if text[i+1] != root_word:
                        new_text.append(text[i])
                        i+=1
                    elif text[i] in self.stopwords:
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



    def bigrams_for_similar_garments(self, text_series, word, num_sim=10):
        '''
        INPUT: text_series => pandas series or list of [lists of word tokens]
            word = a root word
            model = a trained word2vec model or Word2Vec.open('model_path')

        RETURNS: a list of [lists of modified word tokens]
        '''

        root_words = collect_similar(word, self.model, num_sim)
        new_texts = []
        for text in text_series:
            for word in root_words:
                text = make_bigrams(text, word, self.stopwords)
            new_texts.append(text)
        return new_texts


    def bigrams_for_all_garments(self, text_series, num_sim=10):
        '''
        INPUT: text_series => pandas series or list of [lists of word tokens]
            model = a trained word2vec model or Word2Vec.open('model_path')

        RETURNS: a list of [lists of modified word tokens]
        '''

        basic_garments = ["dress", "pants", "shirt", "shoes", "bag"]
        for garment in basic_garments:
            text_series = bigrams_for_similar_garments(text_series, garment, model, stopwords, num_sim)
        return text_series
