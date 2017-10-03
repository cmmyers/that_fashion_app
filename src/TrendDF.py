###############################################################
# Creates the class TrendDF - a dataframe of potential trends.#
# Called from tfa_phase1.py
###############################################################

from collections import Counter


class TrendDF():
    def __init__(self, df):
        print "Loading large dataframe from pickle. Please wait."
        self.df = df
        print 'Creating counter of all words/bigrams'
        self.count = self.make_counter()


    def make_counter(self):
        return Counter([word for desc in \
                                self.df.bigrammified_descs for word in desc])

    def split_on_year(self, year):
        # return a new TrendDF object for one specific year
        return TrendDF(self.df.loc[self.df.year == year])

    def count_term(self, term):
        return self.count[term]

    def term_count_one_year(self, term, year):
        this_df = TrendDF(self.split_on_year(year))
        return this_df.count_term(term)

    def term_count_range_years(self, term, begin_yr, end_yr):
        count_dict = {}
        for yr in xrange(begin_yr, end_yr + 1):
            count = self.term_count_one_year(term, yr)
            print yr, count
            count_dict[yr] = count
        return count_dict

    def find_all_bigrams_above_threshold(self, threshold):
        above_threshold = {}
        for k, v in self.count.iteritems():
            if '_' in k and v > threshold:
                above_threshold[k] = v
        return Counter(above_threshold)

    def get_counts_by_year_all_bg(self, threshold, begin_yr, end_yr):
        this_dict = {}
        for yr in xrange(begin_yr, end_yr + 1):
            this_df = self.split_on_year(yr)
            this_dict[yr] = {}
            for bg in self.find_all_bigrams_above_threshold(threshold).keys():
                this_dict[yr][bg] = this_df.count[bg]
        return this_dict

    def find_big_change(self, earlier_yr, later_yr, multiplier=2, min_v = 50, \
                       verbose = False):
        '''
        multiplier is the minimum ratio of counts for later_yr:earlier_yr
        min_v is the threshold for the count on the item in the later year
        '''
        dict_split_on_years = self.get_counts_by_year_all_bg(50,earlier_yr,\
                                                                    later_yr)
        potential_trends = []
        for k, v in dict_split_on_years[later_yr].iteritems():
            earlier_v = dict_split_on_years[earlier_yr][k]
            if v > multiplier*earlier_v and v > min_v:
                if verbose == True:
                    print '''
                        Term: {}
                        Count in {}: {}
                        Count in {}: {}
                        '''.format(k, later_yr, v, earlier_yr, earlier_v)
                potential_trends.append(k)
        return potential_trends
