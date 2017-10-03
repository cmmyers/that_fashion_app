import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Trend(object):

    def __init__(self, phrase, garment_type=None):
        self.phrase = phrase
        self.type = garment_type


    def plot_by_month(self, df, start_month, start_year, num_months):
        '''
        Creates a plot showing the term frequency of the Trend
        over a given date range, by month, (todo: using a rolling average over 3 months).
        INPUT: dataframe contaiing dates and descriptions,
                starting month and year, number of months to plot
        OUTPUT: matplotlib object
        '''

        tfm, tpm, month_year_tuples = self.get_tfm_tpm(df, 'bigrammified_descs', start_month, start_year, num_months)

        tfm = tfm.rolling(6, 1).mean()
        tpm = tpm.rolling(6, 1).mean()

        y_axis = tfm*1./tpm

        x_axis = self.coerce_to_datetime(month_year_tuples)

        plt.plot(x_axis, y_axis, label=self.phrase)

    def show_plot(self, highlight_year=None):
        '''
        styles the plot created in plot_by_month)
        '''
        plt.legend()
        plt.xticks(rotation = -35, ha='left')
        if highlight_year:
            plt.axvspan(pd.datetime(highlight_year, 1, 1), pd.datetime(highlight_year + 1, 1, 1), color='grey', alpha=0.6)
            plt.axvspan(pd.datetime(highlight_year, 1, 1), pd.datetime(highlight_year + 2, 1, 1), color='grey', alpha=0.3)
        sns.set(rc={'figure.facecolor':'white'})
        plt.ylabel("term frequency / total posts")
        plt.show()

    def differences(self, df, col_name, start_month, start_year, num_months):
        tf_matrix = self.get_tfm_tpm(df, col_name, start_month, start_year, num_months)
        freq_ratio =  tf_matrix[1]*1.0/tf_matrix[2]

        abs_dif_month_over_month = []
        mag_dif_month_over_month = []
        for i in xrange(0, num_months - 12):
            abs_dif_month_over_month.append(freq_ratio[i + 12] - freq_ratio[i])
        for j in xrange(0, num_months - 12):
            mag_dif_month_over_month.append(abs_dif_month_over_month[j]/freq_ratio[j])
        return {'month_yr': tf_matrix[0], 'freq_ratio':freq_ratio, 'abs_dif_m_over_m': abs_dif_month_over_month, \
            'mag_dif_m_over_m': mag_dif_month_over_month}

    def plot_differences(self, df, start_month, start_year, num_months):

        freq_ratio, abs_dif_month_over_month, mag_dif_month_over_month, month_year_tuples = \
               self.differences(df, start_month, start_year, num_months)
        x_axis = self.coerce_to_datetime(month_year_tuples)
        x_axis = x_axis[12:]

        y_axis = mag_dif_month_over_month

        plt.plot(x_axis, y_axis, label= 'magnitude changes yoy by month for {}'.format(self.phrase))

    def differences_yr(self, df, start_year, end_year):
        #it might be interesting to look at combinations of 2 year pairs
        #this wouldn't get too out of control since we won't be looking at more than a 10-yr time span
        tfy, tpy, years = self.get_tfy_tpy(df, start_year, end_year)
        num_yrs = end_year - start_year
        freq_ratio = np.array(tfy * 1.0)/np.array(tpy)
        abs_difs = []
        mag_difs = []
        for i, y in enumerate(xrange(start_year, end_year)):
            abs_dif = freq_ratio[num_yrs] - freq_ratio[i]
            abs_difs.append(abs_dif)
            mag_dif = abs_dif / freq_ratio[i]
            mag_difs.append(("dif {} over {}".format(end_year, y), mag_dif))

        return abs_difs, mag_difs

    def get_tfm_tpm(self, df, col_name, start_month, start_year, num_months):
        '''
        counts the total number of posts in which a given term appears by month
        and the total posts from that month.
        INPUT: dataframe contaiing dates and descriptions, name of column w/ tokenized descriptions,
                starting month and year, number of months to count
        OUTPUT: mo-yr combo tuples (for plotting/indexing), list of term frequencies
                  per month, list of total posts per month
        '''
        mo = start_month
        yr = start_year

        month_year_tuples = []
        for m in range(num_months):
            #create a list of tuples so we can segment our df
            yr_s = str(yr)
            mo_s = str(mo)
            if len(mo_s) == 1:
                mo_s == '0{}'.format(mo_s)

            month_year_tuples.append((yr, mo, 01))

            if mo % 12 == 0:
                yr += 1
                mo = 1
            else:
                mo += 1


        tf_by_mo = []
        tp_by_mo = []
        rnges = []

        #iterate over months
        for tup in month_year_tuples:

            yr_mask = df.year == tup[0]
            df_yr = df[yr_mask]
            mo_mask = df_yr.month == tup[1]
            df_mo = df_yr[mo_mask]
            segment = df_mo[col_name]
            ct = 0
            total = 0
            for row in segment:
                total += 1
                if self.phrase in row:
                    ct+=1
            tf_by_mo.append(ct)

            #so we don't try to divide by 0
            tp_by_mo.append(total + 1)

        tfm = pd.Series(tf_by_mo)
        tpm = pd.Series(tp_by_mo)
        my_tuples = month_year_tuples
        return (tfm, tpm, my_tuples)

    def get_tfy_tpy(self, df, start_year, end_year):
        '''
        counts the total number of posts in which a given term appears over a year
        and the total posts from that year.
        INPUT: dataframe contaiing dates and descriptions, name of column w/ tokenized descriptions,
                starting and ending year
        OUTPUT: list of term frequencies per year, list of total posts per year, list of years
        '''

        tf_by_yr = []
        tp_by_yr = []
        for yr in xrange(start_year, end_year + 1):
            yr_mask = df.year == yr
            df_yr = df[yr_mask]
            segment = df_yr.tokenized_descs
            ct = 0
            total = 0
            for row in segment:
                total += 1
                if self.phrase in row:
                    ct+=1
            tf_by_yr.append(ct)

            #so we don't try to divide by 0
            tp_by_yr.append(total + 1)


        tfy = np.array(tf_by_yr)
        tpy = np.array(tp_by_yr)
        years = xrange(start_year, end_year + 1)
        return tfy, tpy, years

    def coerce_to_datetime(self, series):
        series_2 = []
        for item in series:
            try:
                s = "{}, {}, {}".format(item[0], item[1], item[2])
                series_2.append(s)
            except TypeError:
                series_2.append('2008, 03, 01')
        series_2 = pd.Series(series_2)
        series_3 = pd.to_datetime(series_2)
        return series_3
