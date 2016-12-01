import pandas as pd

def make_yearly_dfs(dfs):
    yearly_dfs = {}
    for year in xrange(2008, 2017):
        all_dfs_this_year = []

        for df in dfs:
            year_mask = df['year'] == year
            df_year = df.loc[year_mask]
            all_dfs_this_year.append(df_year)


        yearly_dfs['df_for_{}'.format(str(year))] =  pd.concat(all_dfs_this_year)


    return yearly_dfs


def pickle_years(dict):
    for k, v in dict.iteritems():
        v.to_pickle('{}.pkl'.format(str(k)))

def combine_new_dfs(dfs, dict):
    old_dfs = []
    combined_dfs = []

    for k, v in dict.iteritems():
        df = pd.read_pickle('{}.pkl'.format(str(k)))
        old_dfs.append(df)

    new_dfs = make_yearly_dfs(dfs)

    for old_df, new_df in zip(old_dfs, new_dfs):
        combined_df = pd.concat([old_df, new_df])
        combined_dfs.append(combined_df)

    
