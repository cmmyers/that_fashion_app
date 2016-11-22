import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Trend(object):

    def __init__(self, phrase, garment_type=None):
        self.phrase = phrase
        self.type = garment_type


    def plot_over_time(self, df, date_begin, num_weeks):
        '''
        Creates a plot showing the term frequency of the Trend
        over a given date range
        INPUT: dataframe contaiing dates and descriptions,
                start and end date in std format ['1980-01-15']
        OUTPUT: matplotlib object
        '''
        start = pd.to_datetime(date_begin)
        term_frequencies_by_day = []
        total_posts_by_day = []
        tf_by_wk = []
        tp_by_wk = []
        rnges = []

        for week in range(num_weeks):
            rnges.append(pd.date_range(start, start + pd.Timedelta(days=7)))
            start = start + pd.Timedelta(days=7)

        for rng in rnges:


            for a_date in rng:
                mask = df.datetime == a_date
                segment = df[mask]
                segment = segment.photo_desc
                ct = 0
                total = 0
                for row in segment:
                    total += 1
                    if self.phrase in row:
                        ct+=1
                term_frequencies_by_day.append(ct)
                total_posts_by_day.append(total)

            wk_tf = sum(term_frequencies_by_day)
            wk_total = sum(total_posts_by_day)
            tf_by_wk.append(wk_tf)
            tp_by_wk.append(wk_total)

            term_frequencies_by_day = []
            total_posts_by_day = []




        tfw = np.array(tf_by_wk)
        tpw = np.array(tp_by_wk)
        dates_by_week = [rng[0] for rng in rnges]

        #plot dates on x axis, frequency on y-axis
        moving_ave = np.convolve(tfw*1./tpw, np.ones(4)/4)[1:num_weeks+1]
        tf_plot = plt.plot(dates_by_week, moving_ave, label=self.phrase)
        return tf_plot
