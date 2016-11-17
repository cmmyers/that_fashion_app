import matplotlib.pyplot as plt

#to do: go back to the source and deal with the date issue there
#get a list of 20 trends for 2008-2009


class Trend(object):

    def __init__(self, phrase, garment_type):
        self.phrase = phrase
        self.type = garment_type


    def plot_over_time(self, df, date_begin, date_end):
        '''
        Creates a plot showing the term frequency of the Trend
        over a given date range
        INPUT: dataframe contaiing dates and descriptions,
                start and end date in std format ['1980-01-15']
        OUTPUT: matplotlib object
        '''

        term_frequencies_by_day = []
        rng = pd.date_range(date_begin, date_end)
        for date in range:
            #create a mini-df for posts on each date in range
            segment = df[df.date == date]
            ct = 0
            for desc in segment:
                if self.phrase in segment.description:
                    ct += 1
            term_frequencies_by_day.append(ct)
        #plot dates on x axis, frequency on y-axis
        tf_plot = plt.plot(rng, term_frequencies_by_day)
        return tf_plot
