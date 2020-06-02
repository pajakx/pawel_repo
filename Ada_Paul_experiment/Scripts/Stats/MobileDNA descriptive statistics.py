# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 12:26:01 2020

MOBILE DNA descriptive statistics


@author: Paweł Jakuszyk
"""
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


data_wide_mDNA =pd.read_csv(r'C:\Users\Pawel\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')

### Screentime ###
# max = 676.5316799999998
# min = 38.26392666666667
# mean = 194.97208000000003
# standard deviation = 145.42111856266771
print(data_wide_mDNA['screentime_mean'].min())
print(data_wide_mDNA['screentime_mean'].max())
print(data_wide_mDNA['screentime_mean'].mean())
print(data_wide_mDNA['screentime_mean'].std())

### SocialMedia ###
# max = 331.4625299999999
# min = 7.948843333333333
# mean = 90.62189111111111
# standard deviation = 85.84626983924129
print(data_wide_mDNA['socialmedia_mean'].min())
print(data_wide_mDNA['socialmedia_mean'].max())
print(data_wide_mDNA['socialmedia_mean'].mean())
print(data_wide_mDNA['socialmedia_mean'].std())