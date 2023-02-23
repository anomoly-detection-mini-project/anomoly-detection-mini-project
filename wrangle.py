# imports

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)


def get_max_traffic(df):
    
    df = df  [~((df.path.str.startswith('/'))|(df.path.str.startswith('appendix')) | (df.path.str.startswith('users'))|(df.path.str.startswith('warmup')))]
    
    df = df[df.name != 'Staff']
    
    df = (df.groupby(['program_id','name'])
            .path.value_counts(normalize=True)
            .rename('proba_status')
            .reset_index())
    
    df_1 = pd.DataFrame(df.groupby(['program_id','name']).proba_status.max()).reset_index()
    
    df = pd.merge(df, df_1, how='inner', on=['program_id','name','proba_status'])
    
    return df