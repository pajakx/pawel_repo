# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:54:49 2020

@author: Paweł Jakuszyk
"""

###### Statistics
from scipy import stats
import statsmodels.api as sm
import os
import pingouin as pg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels
from scipy.stats import spearmanr
from pingouin import mixed_anova, anova, pairwise_tukey
from pingouin import logistic_regression
import pprint
from statsmodels.multivariate.manova import MANOVA
from pingouin import ancova

#import data in long and wide format for different anlysis
data_long = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv')
#Exclude participant 26 as we know that he is way off with amplitudes in this paradigm.
data_long = data_long[data_long.participant != 'P26']
data_long.describe()


data_wide_mDNA =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
#Exclude participant 26 as we know that he is way off with amplitudes in this paradigm.
data_wide_mDNA = data_wide_mDNA[data_wide_mDNA.participant != 'P26']
data_wide_mDNA.describe()



#Trying to get data in the right shape for ancova
dupa = data_long
dupa = dupa[data_long.participant != 'P22']
dupa = dupa[data_long.participant != 'P24']
dupa = dupa.set_index('participant')

df_sm = dupa["socialmedia_mean"].dropna()
df_amp = dupa[["target_maxAmp_Pz",'blocks']].dropna()


Df_for_ancova = df_amp.join(df_sm, how='outer')

Df_for_ancova.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_social_for_ancova.csv')
