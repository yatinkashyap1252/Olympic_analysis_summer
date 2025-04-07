import pandas as pd

def preprocess(df,region_df):
    
    df=df[df['Season']=='Summer']
    
    df=df.merge(region_df,on="NOC",how="left")
    
    df.drop_duplicates(inplace=True)
    
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    
    df[['Gold', 'Silver', 'Bronze']] = df[['Gold', 'Silver', 'Bronze']].astype(int)
    
    return df