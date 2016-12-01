
import string
import pandas as pd

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

def minimal_from_concat(pkl):
    df = pd.read_pickle(pkl)
    df = get_columns_for_nlp(df)
    return df


coll1 = ['posts1002', 'posts1003', 'posts1004', 'posts1005', 'posts1007', 'posts1008']
coll2 = ['posts1009', 'posts1010', 'posts1011', 'posts1012', 'posts1013', 'posts1014']
coll3 = ['posts1015', 'posts1016',  'posts1018', 'posts1019','posts1020']
coll4 = ['posts1021', 'posts1022a', 'posts1022b', 'posts1022c',  'posts1022e']
coll5 = ['posts1024', 'posts1025', 'posts1026', 'posts1027', 'posts1028','posts1029']
coll6 = ['posts1030', 'posts1031', 'posts1033', 'posts1034','posts1035','posts1036']
coll7 = ['posts1037', 'posts1039', 'posts1040', 'posts1041', 'posts1042', 'posts1043', 'posts1044']
coll8 = []
coll9 = ['posts1014a', 'posts1015a', 'posts1016a', 'posts1022d', 'posts1025a', 'posts1026a', 'posts1032', 'posts1045']
