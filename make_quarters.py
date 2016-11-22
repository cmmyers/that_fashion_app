

'''purpose: to take a dataframe and segment it into quarters

'''

def make_year(df, year):
    mask = df.year == year
    return df[mask]

def make_quarter(df, year, quarter):
    year_df = make_year(df, year)
    mask = year_df.quarter == quarter
    return year_df[mask]
