import matplotlib.pyplot as plt
import pandas as pd

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
        print rng

        for a_date in rng:
            mask = df.datetime == a_date
            segment = df[mask]
            segment = segment.photo_desc
            for row in segment:
                ct = 0
                if self.phrase in row:
                    ct+=1
            term_frequencies_by_day.append(ct)

        #plot dates on x axis, frequency on y-axis
        tf_plot = plt.plot(rng, term_frequencies_by_day)
        return tf_plot
