import string
from pymongo import MongoClient
import pandas as pd


coll1 = ['posts1002', 'posts1003', 'posts1004', 'posts1005', 'posts1006', 'posts1007', 'posts1008']
coll2 = ['posts1009', 'posts1010', 'posts1011', 'posts1012', 'posts1013', 'posts1014']
coll3 = ['posts1015', 'posts1016',  'posts1018', 'posts1019','posts1020']
coll4 = ['posts1021', 'posts1022a', 'posts1022b', 'posts1022c',  'posts1022e']
coll5 = ['posts1024', 'posts1025', 'posts1026', 'posts1027', 'posts1028','posts1029']
coll6 = ['posts1030', 'posts1031', 'posts1033', 'posts1034','posts1035','posts1036']
#need 1038
coll7 = ['posts1037', 'posts1039', 'posts1040', 'posts1041', 'posts1042', 'posts1043', 'posts1044']
coll8 = ['posts1006', 'posts1038']
#coll9 tables are on VA2
coll9 = ['posts1014a', 'posts1015a', 'posts1016a', 'posts1022d', 'posts1025a', 'posts1026a', 'posts1032', 'posts1045']

def make_df(database, collection):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database]
    posts = db[collection]
    cursor = posts.find()
    df =  pd.DataFrame(list(cursor))
    clean_up(df)
    get_columns_for_nlp(df)

    return df

def clean_up(df):
    #get the date into fucking recognizable date format
    try:
        df['datetime'] = coerce_to_datetime(df.date)
    except AttributeError:
        pass
    except TypeError:
        df['datetime'] = '2008-03-01'
    #deal with location issues [this should have been solved in chic_clean.py but some are slipping through]

    try:
        df.location.fillna("Somewhere On Earth")
    except AttributeError:
        pass
    except TypeError:
        pass


def coerce_to_datetime(series):
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


def get_columns_for_nlp(df):

    columns = ['post_id', 'photo_desc', 'username', 'location', 'datetime']

    new_df = pd.DataFrame()
    for c in columns:
        new_df[c] = df[c]

    new_df['month'] = df['datetime'].dt.month
    new_df['quarter'] = df['datetime'].dt.quarter
    new_df['year'] = df['datetime'].dt.year
    make_tokens(new_df)

    return new_df

def make_tokens(df):
    #remove punct, lowercase all, remove newline chars and then
    #make a list of all terms in description field and create a new column
    srs = df.photo_desc
    list_o_strings = []
    for item in df.photo_desc:
        item = str(item)
        item = item.translate(None, string.punctuation).lower().replace('\n', ' ').split()
        list_o_strings.append(item)
    df['tokenized_descs'] = list_o_strings


def make_concat_df(db_name, col_list):
    dfs = []
    for col in col_list:
        dfs.append(make_df(db_name, col))
    df = pd.concat(dfs)
    return df


def make_all():
    db = 'parsedB'
    print "Using {}".format(db)
    #db = 'parsecC'
    df1 = make_concat_df(db, coll1)
    print "df1 made"
    df1.to_pickle('concat1b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    df2 = make_concat_df(db, coll2)
    print "df2 made"
    df2.to_pickle('concat2b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    df3 = make_concat_df(db, coll3)
    print "df3 made"
    df3.to_pickle('concat3b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    df4 = make_concat_df(db, coll4)
    print "df4 made"
    df4.to_pickle('concat4b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    df5 = make_concat_df(db, coll5)
    print "df5 made"
    df5.to_pickle('concat5b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    df6 = make_concat_df(db, coll6)
    print "df6 made"
    df6.to_pickle('concat6b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    df7 = make_concat_df(db, coll7)
    print "df7 made"
    df7.to_pickle('concat7b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    df8 = make_concat_df(db, coll8)
    print "df8 made"
    df8.to_pickle('concat8b.pkl')
    raw_input("move this to /dataxvdf before continuing")
    #df8 = make_concat_df(db, coll8)
    #print "df8 made"
    # df8.to_pickle('concat8b.pkl')
    # raw_input("move this to VA1")
    #df9 = make_concat_df(db, coll9)
    #print "df9 made"
    # df9.to_pickle('concat9b.pkl')
    # raw_input("move this to VA1")
