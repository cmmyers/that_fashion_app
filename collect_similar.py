def collect_similar(model_path, word, n_ouput):

    #using a word2vec model find n words most similar to the given words
    #and return as a list [include the original word in the list]
    with open(model_path) as f:
        model = pickle.load(f)

    most_sim = model.most_similar(word, topn=n_output)
    most_sim_list = [item[0] for item in most_sim]

    return most_sim_list
