# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:40:34 2020

.______    _______  __    __       ___   ____    ____  __    ______    __    __  .______          ___       __      
|   _  \  |   ____||  |  |  |     /   \  \   \  /   / |  |  /  __  \  |  |  |  | |   _  \        /   \     |  |     
|  |_)  | |  |__   |  |__|  |    /  ^  \  \   \/   /  |  | |  |  |  | |  |  |  | |  |_)  |      /  ^  \    |  |     
|   _  <  |   __|  |   __   |   /  /_\  \  \      /   |  | |  |  |  | |  |  |  | |      /      /  /_\  \   |  |     
|  |_)  | |  |____ |  |  |  |  /  _____  \  \    /    |  | |  `--'  | |  `--'  | |  |\  \----./  _____  \  |  `----.
|______/  |_______||__|  |__| /__/     \__\  \__/     |__|  \______/   \______/  | _| `._____/__/     \__\ |_______|
                                                                                                                    

@author: PJ

"""
##### to concat the existing participants data into one dataset
from glob import glob
import pandas as pd

filenames = glob(r'C:\Users\user\Desktop\FOCUS\behavioral\P*.csv')


dataframes = [pd.read_csv(f) for f in filenames]

finaldf = pd.concat(dataframes, axis=0)

#print(dataframes)

finaldf.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\P_Merged1.csv', index = None, header=True)


####### getting the data ready


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df1 = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\P_Merged1.csv')

data_merged = df1[['participant','sounds','blocks','corrAns','key_resp_trial.keys','number','key_resp_trial.corr','key_resp_trial.rt']]
data_merged = data_merged.rename(columns={"key_resp_trial.corr": "key_resp_corr", "key_resp_trial.rt": "key_resp_rt",'key_resp_trial.keys':'key_resp_key'})
data_merged = data_merged.replace(
        
        
   ['sounds/buzz.wav', 'sounds/neutral.wav', 'sounds/silence.wav',
    'conditions_CPT_60_neutral.xlsx','conditions_CPT_60_buzz.xlsx',
    'conditions_CPT_60_nodis.xlsx','1.12.08.1993franer120','15','19',
    '2.18.10.1995MAKAAL60','P21.1','23','3.07.06.1997FRRUAN600',
    '4.06.06.1993MAKAGE120', '5_07_04_1998LYMIRO120','6_26_03_1997KRYUGO90',
    'p7','30',],
                                  
   ['buzz','neutral', 'silence','neutral_block','buzz_block','nodis_block','P1','P15',
    'P19','P2','P21','P23','P3','P4','P5','P6','P7','P30',]
   
   
   )



data_merged.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\P_Merged.csv', index = None, header=True)


###### Adding variables

df_corr = data_merged.loc[(data_merged.corrAns == 'space') & (data_merged.key_resp_corr == 1), ['key_resp_rt']]
#adding a new clumn with desired variable
data_merged['corr_rt'] = df_corr

#omission error create a variable
data_merged.loc[(data_merged.number == 3) & (data_merged.key_resp_corr == 0),'om_err'] = 1
# false alarms create a variable
data_merged.loc[(data_merged.number != 3) & (data_merged.key_resp_key == 'space'),'false_alarm'] = 1

data_merged.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\P_Merged_var.csv', index = None, header=True)


'''
####### some plots
ax = sns.catplot(x="blocks", y="corr_rt",hue='participant', data=data_merged, kind='point',aspect=1.5)
ax1 = sns.catplot(x="blocks", y="false_alarm",hue='participant', data=data_merged, kind = 'bar', estimator = sum, aspect=1.5)
ax2 = sns.catplot(x="blocks", y="om_err", data=data_merged, kind = 'bar', estimator = sum, aspect=1.5 )
'''
########################################
#Create means per participant per block#
########################################

#Correct response time mean per participant per block

data_merged.loc[(data_merged.blocks == 'nodis_block') & (data_merged.key_resp_corr == 0),'om_err'] = 1










###### Statistics


import os
import pingouin as pg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels
from pingouin import mixed_anova, anova, pairwise_tukey
from pingouin import logistic_regression


data_merged = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\P_Merged_var.csv')

### Fill in Nan values in false alarm and omission error (0)
data_merged=data_merged.fillna({'false_alarm':0, 'om_err':0})
#data_merged.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\P_Merged_var.csv', index = None, header=True)

# ANOVA - does correct reaction time differ between blocks?
aov_corr_rt = anova(dv='corr_rt', between='blocks', data=data_merged)

print(aov_corr_rt)

rep_anov_alarm = pg.rm_anova(data=data_merged, dv='false_alarm', within= 'blocks', subject='participant', detailed=True)


# follow-up pairwise comparison 
pairs_corr_rt = pairwise_tukey(dv='corr_rt', between='blocks', data=data_merged)

print(pairs_corr_rt)

#### ANOVA - does false alarms differ between blocks?
aov_alarms = anova(dv='false_alarm', between='blocks', data=data_merged)

print(aov_alarms)

# follow-up pairwise comparison 
pairs_alarms = pairwise_tukey(dv='false_alarm', between='blocks', data=data_merged)

print(pairs_alarms)
######## ANOVA - does omission errors differ between blocks?
aov_omission = anova(dv='om_err', between='blocks', data=data_merged)

print(aov_omission)

# follow-up pairwise comparison 
pairs_omission = pairwise_tukey(dv='om_err', between='blocks', data=data_merged)

print(pairs_omission)

## Something
data_merged.dtypes
##data_merged["false_alarm"] = pd.to_numeric(data_merged["false_alarm"])
#data_merged.count()
#convert specific columns
data_merged = data_merged.astype({"blocks" : str})
#lr_1 = logistic_regression(data_merged["blocks"], data_merged["false_alarm"])