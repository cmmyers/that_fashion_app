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
        start_year == str(start_year)
        if len(str(start_month)) == 1:
            start_month = str(0) + str(start_month)
        else:
            start_month = str(start_month)

        start = pd.to_datetime('{}{}01'.format(start_year, start_month))

        term_frequencies_by_day = []
        total_posts_by_day = []
        tf_by_mo = []
        tp_by_mo = []
        rnges = []

        for month in range(num_months):
            #create a list of date ranges, one item for each months
            rnges.append(pd.date_range(start, start + pd.Timedelta(days=30)))
            start = start + pd.Timedelta(days=30)

        #iterate over months
        for rng in rnges:
            #iterate over dates in month
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

            mo_tf = sum(term_frequencies_by_day)
            mo_total = sum(total_posts_by_day)
            tf_by_mo.append(mo_tf)
            tp_by_mo.append(mo_total)
            #reset term frequencies by day
            term_frequencies_by_day = []
            total_posts_by_day = []


        tfm = np.array(tf_by_mo)
        tpm = np.array(tp_by_mo)


        y_axis = tfm*1./tpm
        #density = gaussian_kde(y_axis)
        x_axis = [rng[0] for rng in rnges]
        #density.covariance_factor = lambda : .25
        #density._compute_covariance()
        #plt.plot(xs,density(xs))

        #rolling average. first term mean of months 1 & 2; last (nth) term mean of n-1 & n
        #all others mean of k-1, k, k+1
        y_axis[0] = np.mean(y_axis[0:1])
        y_axis[-1] = np.mean(y_axis[-2:-1])
        y_axis[1:-2] = [np.mean(y_axis[i-1:i+1]) for i in range(len(y_axis[1:-2]))]

        #plot dates on x axis, frequency on y-axis
        #moving_ave = np.convolve(tfw*1./tpw, np.ones(4)/4)[1:num_weeks+1]
        plt.plot(x_axis, y_axis, label=self.phrase)

    
