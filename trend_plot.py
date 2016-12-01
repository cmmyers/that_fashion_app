def six_mo_plot(year, start_q, term):
    '''
    Take a year and a quarter (1 through 4) and outputs plots for the 10 most
    frequent words to precede the given term during the six month period beginning that quarter
    '''


    q1 = quarter_dfs['{}_q{}'.format(year, start_q)]
    if start_q == 4:
        q2 = quarter_dfs['{}_q{}'.format(year + 1, 1)]
    else:
        q2 = quarter_dfs['{}_q{}'.format(year, start_q + 1)]

    df_this = pd.concat([q1, q2])

    tokens = tokenize(df_this)
    finder, bigram_measure = bigrams_colloc(tokens)

    top_freq = []
    while len(top_freq) < 10:
        for phrase in finder.nbest(bigram_measure.raw_freq, 100000):
            if str(phrase[1]) == term and str(phrase[0]) not in all_sw:
                top_freq.append(phrase)

    for ind in range(10):
        this_trend = top_freq[ind]
        this_trend = "{} {}".format(this_trend[0], this_trend[1])
        this_trend_ob = Trend(this_trend)

        print this_trend_ob.phrase

        #'df' refers to the master dataframe holding all data.
        this_trend_ob.plot_over_time(df, '2008-06-30', 208)
        plt.legend()
        plt.xticks(rotation=-35)
        plt.axvspan(df_this.datetime.min(), df_this.datetime.max(), color='blue', alpha=0.5)

        plt.show()
