import pandas as pd
from TrendDF import TrendDF

def create_TrendDF(path_to_pkl_df):
    df = pd.read_pickle(path_to_pkl_df)
    return TrendDF(df)


if __name__ == '__main__':
    #dfX_train, model = create_TrendDF(2009,2012)
    print '''
    create a TrendDF object by passing a path to a pickled dataframe:
    trenddf = create_TrendDF(path_to_pkl_df)
    '''
