# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:52:34 2020

___  ___      _     _ _     ______ _   _   ___  
|  \/  |     | |   (_) |    |  _  \ \ | | / _ \ 
| .  . | ___ | |__  _| | ___| | | |  \| |/ /_\ \
| |\/| |/ _ \| '_ \| | |/ _ \ | | | . ` ||  _  |
| |  | | (_) | |_) | | |  __/ |/ /| |\  || | | |
\_|  |_/\___/|_.__/|_|_|\___|___/ \_| \_/\_| |_/
                                                
                                                
                                                                                                
@author: Paweł Jakuszyk
"""

import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
from matplotlib import pyplot as plt
import seaborn as sns
sns.set();
from tqdm import tqdm   #progressbar
tqdm.pandas()   #progressbar instantiëren voor pandas

##Read the filepaths
app_filename = r"C:\Users\user\Desktop\FOCUS_EXP\focus_paul_ada_appevents.csv"
notif_filename = r"C:\Users\user\Desktop\FOCUS_EXP\focus_paul_ada_notifications.csv"
##Create a new dataframe for the desired variables
final = pd.read_excel(r'C:\Users\user\Desktop\FOCUS_EXP\finalmobDNA.xlsx')

##Load in appevent file
df = pd.read_csv(app_filename, sep=";", parse_dates=['startTime', 'endTime'])

##Drop unnecessary columns
df.drop(columns=['Unnamed: 0','latitude','longitude'], inplace=True)
#df.info()

#Check for dubbles
dubbels = pd.concat(g for _, g in df.groupby(["application","startTimeMillis","endTime"]) if len(g) > 1)

##Drop duplicated values
df = df.drop_duplicates(["startTime","application","endTime"])

# Convert columns to datetime object
df['startTime'] = pd.to_datetime(df['startTime'])
df['endTime'] = pd.to_datetime(df['endTime'])

# Create a date variable
df['day'] = df.startTime.dt.date

#number of days logged per participant

# # Group by participnt, look at totally unique days logged, per person
final["log"] = df.groupby('surveyId')['day'].nunique('day')

## Create variable duration: end time - start time, / 1000 (in seconds)
df['duration'] = (df.endTimeMillis - df.startTimeMillis)/1000

# Total and average duration per day
df.groupby(["surveyId","day"]).duration.agg(['sum', 'mean'])

# Average time (sec) over days, per participant
final["perday_sec"] = df.groupby(["surveyId","day"])['duration'].sum().groupby('surveyId').mean()

#######Hours daily on smartphone############
df['day'] = df.endTime.dt.date

pp = df.groupby(['surveyId','day'])['duration'].sum()/3600 
pp

#how many hours a day on avergae per participant
final['meanHday'] = pp.groupby('surveyId').mean()


#Average number of apps used per day

