#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:53:46 2019

@author: lefebvre1217
"""

### Load libaries

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import timeit 
from datetime import datetime 



### Load data
df = pd.read_csv('~/desktop/Provider_Data.txt', sep="|")


def _getToday():
    return datetime.now().strftime("%Y_%m_%d_%HH%MM")


def master_list(x,stops,thres_count, counts):
    x = x.dropna(thresh=thres_count)
    x = x.Service_Provider_Name.value_counts()

    x = x.to_frame().reset_index()
    x.columns = ['Service_Provider_Name', 'Counts']
    
    x = x[x.Counts > counts]
    
    x = x.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    x = x.apply(lambda x: x.str.rstrip() if x.dtype == "object" else x)
    
    x['Service_Provider_Name'] = x['Service_Provider_Name'].str.upper()
    x = x.sort_values(by=['Service_Provider_Name'])
    x['Service_Provider_Name'] = x['Service_Provider_Name'].str.replace("|".join(stops), "")   

    
    ### Run sequence to clean field ###
    x = x.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    x.Service_Provider_Name = x.Service_Provider_Name.str.replace(' ', '_')    


    x.Service_Provider_Name = x.Service_Provider_Name.str.replace("_"," ")

    x['Service_Provider_Name'] = x['Service_Provider_Name'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    x = x.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    
    ### Drop NAN BLANK OR NA FIELDS ###
    x = x[pd.notnull(x['Service_Provider_Name'])]

    ### Drop White Space

    x.Service_Provider_Name.replace('', np.nan, inplace=True)
    x.Service_Provider_Name.dropna(inplace=True)
    
    x.Service_Provider_Name.replace('', np.nan, inplace=True)
    x.Service_Provider_Name.dropna(inplace=True)
    x.dropna(subset=['Service_Provider_Name'], how='all', inplace = True)

    x = x.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    x = x.apply(lambda x: x.str.rstrip() if x.dtype == "object" else x)


    #drop duplicates to create unique master list and assign new field Provider Entity ID
    x = x.drop_duplicates(subset=['Service_Provider_Name'], keep='first')
    x['Provider_Entity_ID'] = np.random.randint(1000,1000000, size=len(x))
    
    return x




def filter_list(x,y):
    
    x = x.sample(y, replace=True)


    x['Service_Provider_Name'] = x['Service_Provider_Name'].str.upper()
    x = x.sort_values(by=['Service_Provider_Name'])


    ### Run sequence to clean field ###
    x = x.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    x.Service_Provider_Name = x.Service_Provider_Name.str.replace(' ', '_')    

    x.Service_Provider_Name = x.Service_Provider_Name.str.replace("_"," ")

    x['Service_Provider_Name'] = x['Service_Provider_Name'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    x = x.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    x = x.apply(lambda x: x.str.rstrip() if x.dtype == "object" else x)


    ### DROP NAN BLANK OR NA FIELDS ###
    x = x[pd.notnull(x['Service_Provider_Name'])]

    ### Drop White Space

    x.Service_Provider_Name.replace('', np.nan, inplace=True)
    x.Service_Provider_Name.dropna(inplace=True)

    x = x.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    x = x.apply(lambda x: x.str.rstrip() if x.dtype == "object" else x)


    x.Service_Provider_Name.replace('', np.nan, inplace=True)
    x.Service_Provider_Name.dropna(inplace=True)
    x.dropna(subset=['Service_Provider_Name'], how='all', inplace = True)
    
    return x


def fuzzy_match(x,choices,scorer,cutoff):
    return process.extractOne(
            x, choices=choices, scorer=scorer, score_cutoff=cutoff)
    
    
def match_back(x,ml,path,filename):
    x = pd.DataFrame({'Original_Index':x.index, 'matched':x.values})
    x = x[x.matched.astype(str) != 'None']
    x = pd.concat([x,x.matched.astype(str).str.split(',',expand=True)],1)
    x[0] = x[0].str.replace('\'|\(', '')
    x[2] = x[2].str.replace('\)', '').astype(int)
    x.rename(columns={0:'Service_Provider_Name', 1:'Probability',2:'Bulk_Index'}, inplace=True)
    ml['Original_Index'] = ml.index
    Output = pd.merge(ml,x, how='inner', on='Original_Index')
    Output.to_csv(path + "Output" + filename, index=False)
    return Output
    


stops = ['AND AQUATIC', 'LLC', 'CENTERS', 'CENTER', 'CEN','VALLEY','VAL','LABRATORIES', 'LABRATORY','LAB', 'CRNA', 'ANRP',
         'MD', 'DC', 'DO', 'PC', 'D0', 'PLLC', 'PLC', 'LTD', 'DPM', 'SPECIALIST', 'SPECIAL', 'SPECI', 'SERVICES', 'SERVICE', 'GROUP',
         'FNP', 'INC', 'ASSOCIATES','ASSOCIATE','ASSOCIA', 'HSP', 'SERVICES','SERVICE', 'PA','SURGERIES', 'SURGERY', 'SURG','CTR',
         'CT', 'PA']


filename = "%s_%s.%s" % ("",_getToday(),"csv")

path = '/users/lefebvre1217/desktop/'

thres_count = 1
counts = 4
fuzz_thres = 75
sample_n = 10000


def main():
    ml = master_list(df, stops, thres_count, counts)
    fl = filter_list(df, sample_n)
    FuzzyWuzzyResults = ml.loc[:, 'Service_Provider_Name'].apply(fuzzy_match,
                            args = (fl.loc[:, 'Service_Provider_Name'],
                                    fuzz.ratio,fuzz_thres))
    complete = match_back(FuzzyWuzzyResults,ml,path,filename)

    

if __name__ == '__main__':
    main()