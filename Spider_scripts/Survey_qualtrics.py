# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:11:06 2020


                                                     _           _     
                                                    | |         (_)    
  ___ _   _ _ ____   _____ _   _    __ _ _ __   __ _| |_   _ ___ _ ___ 
 / __| | | | '__\ \ / / _ \ | | |  / _` | '_ \ / _` | | | | / __| / __|
 \__ \ |_| | |   \ V /  __/ |_| | | (_| | | | | (_| | | |_| \__ \ \__ \
 |___/\__,_|_|    \_/ \___|\__, |  \__,_|_| |_|\__,_|_|\__, |___/_|___/
                            __/ |                       __/ |          
                           |___/                       |___/          



@author: Paweł Jakuszyk
"""


import pandas as pd


data_clean = pd.read_csv(r'C:\Users\Pawel\Documents\Python Scripts\Survey\Survey_nice.csv')

print(data_clean)

print(data_clean["participant"])


###Exclude participants
#data_clean =data_clean.loc[data_clean['participant'] !='P6']

###Count by gender
# Female = 16
# Male = 15
print(data_clean['gender'].value_counts()['Male'])
print(data_clean['gender'].value_counts()['Female'])

### Education ###
# Master's = 23
# Bachelor's = 7
# Elementary = 1
print(data_clean['education'].value_counts()["Master's"])
print(data_clean['education'].value_counts()["Bachelor's"])
print(data_clean['education'].value_counts()["Elementary"])

### Age ###
# max = 47
# min = 19
# mean = 27.70967741935484
# standard deviation = 5.809151104863755
print(data_clean['age'].min())
print(data_clean['age'].max())
print(data_clean['age'].mean())
print(data_clean['age'].std())




