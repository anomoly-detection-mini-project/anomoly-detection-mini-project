# imports

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)





def get_program_max_traffic(df):
    
    '''takes a dataframe
    return a dataframe with maximum traffic visit by program
    '''
    
    df = df  [~((df.path.str.startswith('/'))|(df.path.str.startswith('appendix')) | (df.path.str.startswith('users'))|(df.path.str.startswith('warmup')))]
    df = df[df.name != 'Staff']
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


def Q_two(df):
    '''this function answers questions 2 from the email. it takes in a df and returns
       a new df with a groupby of the names of cohorts and path counts'''
    weird_df= df.groupby(['name', 'path']).agg('count')
    weird_df.sort_values(by= 'name', ascending= False)
    weird_df= weird_df.reset_index()
    weird_df= weird_df[weird_df.path != '/']
    count_df= weird_df[['name', 'path', 'ip']]
    count_df.sort_values(by= ['name', 'ip'], ascending= [False, False])
    new_df= count_df.sort_values(by= 'ip', ascending= False).groupby('name').nth(0)
    return new_df


def plot_q2(new_df):
    '''
    plot for q2
    '''
    ax = sns.scatterplot(data=new_df)
    plt.title('Lesson Vs Cohort?')
    plt.ylabel('Log Count')
    plt.xlabel('Cohorts')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        bottom=False,      # ticks along the bottom edge are off
        labelbottom=False) # labels along the bottom edge are off
    ax.annotate('Toc/Jupiter Cohort', xy=(22.75, 1830), xytext=(3, 1650),
                arrowprops=dict(facecolor='black', shrink=0.09))
    ax.get_legend().remove()
    plt.show()


def q5():
    '''
    this function will subset the data for question 5 and plot the results
    '''
    df=pd.read_csv('curriculum.csv')
    df.rename(columns={'date': 'request_date', 'time': 'request_time'}, inplace=True)
    df=df.dropna()
    df.request_date = pd.to_datetime(df.request_date)
    df = df.set_index(df.request_date)
    df['year'] = df.request_date.dt.year
    my_df=df[(df['year']==2018)|(df['year']==2019)|(df['year']==2020)]
    dsdf=my_df[my_df['program_id']==3]
    devdf=my_df[(my_df['program_id']==2)]
    dsdev=dsdf[dsdf['path'].str.contains('java')]
    devds=devdf[devdf['path'].str.contains('pandas')]
    hits=dsdev['path'].resample('D').count()
    hits.plot(alpha=.75, label='Data Science')
    hits=devds['path'].resample('D').count()
    hits.plot(alpha=.5, label='Web Dev')
    plt.xlabel('Request Date')
    plt.ylabel('Activity')
    plt.title('Cross Discipline Curriculum Access')
    plt.legend()