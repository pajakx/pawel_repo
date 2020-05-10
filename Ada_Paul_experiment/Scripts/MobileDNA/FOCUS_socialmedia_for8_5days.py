# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:57:37 2020

@author: AA
"""

import numpy as np
import datetime as dt
from datetime import timedelta
from matplotlib import pyplot as plt
import seaborn as sns
sns.set();
from tqdm import tqdm   #progressbar
tqdm.pandas()
import pandas as pd

##### Load files
app_filename = r'C:\Users\user\Desktop\MobileDNA\focus_appevents_all.csv'


### df = appevens
# Drop events 
df = pd.read_csv(app_filename, sep=";", parse_dates=['startTime', 'endTime'])
df.drop("Unnamed: 0", axis=1, inplace=True)
df.info()

#Check for dubbels
dubbels = pd.concat(g for _, g in df.groupby(["application","startTimeMillis","endTime"]) if len(g) > 1)
dubbels['session'].value_counts().describe()
df.session.nunique()
# Drop appevents duplicates
df = df.drop_duplicates(
    ["id", "session", "application", "startTimeMillis", "endTimeMillis"]
)

app_social = [
    "com.facebook.katana",  # 1. Facebook
    "com.facebook.lite",  # 1. Facebook (lite)
    "com.facebook.orca",  # 2. Messenger
    "com.facebook.mlite",  # 2. Messenger lite
    "com.instagram.android",  # 3. Instagram
    "com.whatsapp",  # 4. Whatsapp
    # 5. SMS-apps
    "com.snapchat.android",  # 6. snapchat,
    "com.twitter.android",  # 7. Twitter
    "com.linkedin.android",  # 8. LinkedIn
    "com.pinterest",  # 9. Pinterest
    "com.tumblr",  # 10. Tumblr
    "com.google.android.youtube",  # 11. Youtube
]

df = df[df["application"].isin(app_social)]


# Replace surveyId names

df = df.replace(
        
        
   ['12081993franer', #P1
    '18101995makaal', #P2
    '06061997frruan', #P3
    '06061993makage', #P4
    '07041988lymiro', #P5 
    '31011990dailwa', #P7
    '21061991jegrjo', #P8
    '22101987saelke', #P9
    '27081994gaviku', #P10
    '24021999isemha', #P11
    '23051992matipa', #P12
    '30051994macawi', #P13
    '31011992jochfr', #P14
    '14051995emchph', #P15
    '09031993kakane', #P16
    '11081977armaer', #P17
    '02101991albaja', #P18     
    '25072000loemha', #P19
    '08061992hakisa', #P20
    '12121996desebh', #P21
    '19071996chkasa', #P23
    '01101984sacach', #P25
    '30091986manaha', #P26
    '13041985leanro', #P27
    '10061994sashsa', #P28
    '01011992mdraku', #P29
    '18051993soshab',], #P30
                                  
   ['P1',
    'P2',
    'P3',
    'P4',
    'P5',
    'P7',
    'P8',
    'P9',
    'P10',
    'P11',
    'P12',
    'P13',
    'P14',
    'P15',
    'P16',
    'P17',
    'P18',
    'P19',
    'P20',
    'P21',
    'P23',
    'P25',
    'P26',
    'P27',
    'P28',
    'P29',
    'P30']
   

   )



####################
# ADDING VARIABLES #
####################


df['date'] = pd.to_datetime(df['startTimeMillis'], unit='ms').dt.date

df['duration'] = (df.endTimeMillis - df.startTimeMillis)/1000

#df['day'] = df.startTime.dt.day



##############
# APPEVENTS #
##############  

total_screentime_perID = df.groupby(by=['surveyId']).duration.sum()


#### Minutes spent on smartphone per day

pp1=df.groupby(['surveyId','date'])['duration'].sum()/60 #minutes 
pp2 =  pp1.reset_index()


# Rename the column duration to screentime_sum
sum= pp2.rename(columns={"duration": "socialmedia_sum"})

# Rank days from 1 to n...days
#sum['day_nr']= sum.groupby('surveyId')['day'].rank(method='first')
sum.sort_values(['surveyId', 'date'], ascending=[True, False])
sum['date_rank'] =sum.groupby(['surveyId']).apply(lambda x: x['date'].astype('category',ordered=False).cat.codes+1).values

##############
# pick 7days #
##############


days = [2,3,4,5,6]
sum1= sum.date_rank.isin(days)
sum_days = sum[sum1]
sum_days.shape

sum_days1=sum_days.loc[sum_days['surveyId'] == 'P8']


#Drop useless columns
drop=sum_days1.drop(['date', 'date_rank'], axis=1)

# Couting mean for all participants - IN MINUTES
mean=drop[['surveyId','socialmedia_sum']].groupby('surveyId').mean()
mean1=mean.reset_index()

final= mean1.rename(columns={"socialmedia_sum": "socialmedia_mean", "surveyId": "participant" })

# Save to csv
final.to_csv(r'C:\Users\user\Desktop\MobileDNA\socialmedia_mean_all_forP8_5days.csv', index = None, header=True)








