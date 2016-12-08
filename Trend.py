import numpy as np

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

        data = tfw*1./tpw
        density = gaussian_kde(data)
        xs = dates_by_week
        density.covariance_factor = lambda : .25
        density._compute_covariance()
        plt.plot(xs,density(xs))


        #plot dates on x axis, frequency on y-axis
        #moving_ave = np.convolve(tfw*1./tpw, np.ones(4)/4)[1:num_weeks+1]
        plt.plot(dates_by_week, tfw*1./tpw, label=self.phrase)


    def plot_by_week(self, df, date_begin, num_weeks):
        '''
        Creates a plot showing the term frequency of the Trend
        over a given date range, by week, using a rolling average over 4 weeks.
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

        data = tfw*1./tpw
        density = gaussian_kde(data)
        xs = dates_by_week
        density.covariance_factor = lambda : .25
        density._compute_covariance()
        plt.plot(xs,density(xs))


        #plot dates on x axis, frequency on y-axis
        #moving_ave = np.convolve(tfw*1./tpw, np.ones(4)/4)[1:num_weeks+1]
        plt.plot(dates_by_week, tfw*1./tpw, label=self.phrase)


    def plot_by_month(self, df, start_month, start_year, num_months):
        '''
        Creates a plot showing the term frequency of the Trend
        over a given date range, by month, (using a rolling average over 3 months).
        INPUT: dataframe contaiing dates and descriptions,
                starting month and year, number of months to plot
        OUTPUT: matplotlib object
        '''

        tfm, tpm, month_year_tuples = self.get_tpm_tfm(df, start_month, start_year, num_months)

        y_axis = tfm*1./tpm

        x_axis = coerce_to_datetime(month_year_tuples)

        plt.plot(x_axis, y_axis, label=self.phrase)

    def differences(self, df, start_month, start_year, num_months):
        tfm, tpm, month_year_tuples = self.get_tpm_tfm(df, start_month, start_year, num_months)
        freq_ratio = np.array(tfm * 1.0)/np.array(tpm)
        abs_dif_month_over_month = []
        mag_dif_month_over_month = []
        for i in xrange(0, num_months - 12):
            abs_dif_month_over_month.append(freq_ratio[i + 12] - freq_ratio[i])
        for j in xrange(0, num_months - 12):
            mag_dif_month_over_month.append(abs_dif_month_over_month[j]/freq_ratio[j])
        return freq_ratio, abs_dif_month_over_month, mag_dif_month_over_month, month_year_tuples

    def plot_differences(self, df, start_month, start_year, num_months):

        freq_ratio, abs_dif_month_over_month, mag_dif_month_over_month, month_year_tuples = \
               self.differences(df, start_month, start_year, num_months)
        x_axis = coerce_to_datetime(month_year_tuples)
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

    def get_tpm_tfm(self, df, start_month, start_year, num_months):
        '''
        Creates a plot showing the term frequency of the Trend
        over a given date range, by month, (using a rolling average over 3 months).
        INPUT: dataframe contaiing dates and descriptions,
                starting month and year, number of months to plot
        OUTPUT: matplotlib object
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
            segment = df_mo.photo_desc
            ct = 0
            total = 0
            for row in segment:
                total += 1
                if self.phrase in row:
                    ct+=1
            tf_by_mo.append(ct)


            #so we don't try to divide by 0
            tp_by_mo.append(total + 1)


        tfm = np.array(tf_by_mo)
        tpm = np.array(tp_by_mo)
        my_tuples = month_year_tuples
        return tfm, tpm, my_tuples

    def get_tfy_tpy(self, df, start_year, end_year):
        tf_by_yr = []
        tp_by_yr = []
        for yr in xrange(start_year, end_year + 1):
            yr_mask = df.year == yr
            df_yr = df[yr_mask]
            segment = df_yr.photo_desc
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
