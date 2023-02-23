# imports

import pandas as pd
import numpy as np

from env import get_connection
import os


def acquire_data():
    
    '''read data from csv file of a local storage if exists. If csv file does not exist, read data from 
    server using SQL, write data into csv file for cache. Return a dataframe
    '''
    
    filename = 'curriculum.csv'
     
    if os.path.exists(filename):
        # read data from csv file of a local storage
        df = pd.read_csv(filename)
    else: 
        query = '''
                SELECT c.id, c.name, c.start_date, c.end_date,c.program_id, l.date, l.time,l.path,user_id,l.ip
                FROM cohorts as c 
                Right JOIN logs as l  
                ON c.id = l.cohort_id;
                '''

        url = get_connection('curriculum_logs')

        # read data from server using SQL
        df = pd.read_sql(query, url)
        
        # write to data csv file for cache
        df.to_csv('curriculum.csv', index_label=False)
        
    return df