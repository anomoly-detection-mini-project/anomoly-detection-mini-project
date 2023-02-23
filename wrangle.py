# imports

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)


def get_program_cohort_max_traffic(df):
    
    '''takes a dataframe
    return a dataframe with maximum traffic visit by program and cohort
    '''
    
    df = df  [~((df.path.str.startswith('/'))|(df.path.str.startswith('appendix')) | (df.path.str.startswith('users'))|(df.path.str.startswith('warmup')))]
    
    df = df[df.name != 'Staff']
    
    df = (df.groupby(['program_id','name'])
            .path.value_counts(normalize=True)
            .rename('proba_status')
            .reset_index())
    
    df_1 = pd.DataFrame(df.groupby(['program_id','name']).proba_status.max()).reset_index()
    
    df = pd.merge(df, df_1, how='inner', on=['program_id','name','proba_status'])
    
    return df


def get_program_max_traffic(df):
    
    '''takes a dataframe
    return a dataframe with maximum traffic visit by program
    '''
    
    df = df  [~((df.path.str.startswith('/'))|(df.path.str.startswith('appendix')) | (df.path.str.startswith('users'))|(df.path.str.startswith('warmup')))]
    
    df = (df.groupby(['program_id'])
            .path.value_counts(normalize=True)
            .rename('proba_status')
            .reset_index())
    
    df_1 = pd.DataFrame(df.groupby(['program_id']).proba_status.max()).reset_index()
    
    df = pd.merge(df, df_1, how='inner', on=['program_id','proba_status'])
    
    return df

def min_traffic(df):
    
    '''takes a dataframe
    return a dataframe with minimum traffic visit
    '''
    
    df = df  [~((df.path.str.startswith('/'))|(df.path.str.startswith('appendix')) | (df.path.str.startswith('users'))|(df.path.str.startswith('warmup')))]
    df = pd.DataFrame(df.path.value_counts().rename('count'))
    return df