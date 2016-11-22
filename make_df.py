import string
from pymongo import MongoClient
import pandas as pd

def make_df(database, collection):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database]
    posts = db[collection]
    cursor = posts.find()
    df =  pd.DataFrame(list(cursor))
    del df['_id']
    add_columns(df)
    clean_up(df)
    return df

def add_columns(df):

    df['desc_length'] = [len(desc) for desc in df['photo_desc'].values]
    df['num_subphotos'] = [0 if entry=='No Subphotos' else len(entry) for entry in df['subphotos']]
    #get the date into fucking recognizable date format
    df['datetime'] = coerce_to_datetime(df.date)

    df['year'] = df['datetime'].dt.year
    df['quarter'] = df['datetime'].dt.quarter

def clean_up(df):
    #remove punct, lowercase all, remove newline chars and then
    #make a list of all terms in description field and create a new column
    srs = df.photo_desc
    list_o_strings = []
    for item in df.photo_desc:
        item = str(item)
        item = item.translate(None, string.punctuation).lower().replace('\n', ' ').split()
        list_o_strings.append(item)
    df['clean_descs'] = list_o_strings

    #get the date into fucking recognizable date format
    df['datetime'] = coerce_to_datetime(df.date)

    #deal with location issues [this should have been solved in chic_clean.py]
    df.location.fillna("Somewhere On Earth")

def coerce_to_datetime(series):
    series_2 = []
    for item in series:
        s = "{}, {}, {}".format(item[0], item[1], item[2])
        series_2.append(s)
    series_2 = pd.Series(series_2)
    series_3 = pd.to_datetime(series_2)
    return series_3

def make_concat_df(db_name, col_list):
    dfs = []
    for col in col_list:
        dfs.append(make_df(db_name, col))
    df = pd.concat(dfs)
    return df
