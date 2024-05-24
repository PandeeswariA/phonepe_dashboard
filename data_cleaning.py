import pandas as pd

def clean_data(df):
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle numerical columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    num_null = df[numeric_cols].isnull().sum()
    num_null = num_null[num_null > 0]
    for col in num_null.index:
        if df[col].skew() > 0.5 or df[col].skew() < -0.5:
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)
    
    # Handle categorical columns
    cat = df.select_dtypes(include=["object", "category", "bool"])
    cat_null = cat.isnull().sum()
    cat_null = cat_null[cat_null > 0]
    for col in cat_null.index:
        df[col].fillna(df[col].mode()[0], inplace=True)
    
    return df
