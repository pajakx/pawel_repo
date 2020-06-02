# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:44:35 2020

  _____ _        _       
/  ___| |      | |      
\ `--.| |_ __ _| |_ ___ 
 `--. \ __/ _` | __/ __|
/\__/ / || (_| | |_\__ \
\____/ \__\__,_|\__|___/
                        
                        
       _       _        
      | |     | |       
 _ __ | | ___ | |_ ___  
| '_ \| |/ _ \| __/ __| 
| |_) | | (_) | |_\__ \ 
| .__/|_|\___/ \__|___/ 
| |                     
|_|                     

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
data_long = pd.read_csv(r'C:\Users\Pawel\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv')
#Exclude participant 26 as we know that he is way off with amplitudes in this paradigm.
data_long = data_long[data_long.participant != 'P26']
data_long.describe()


data_wide_mDNA =pd.read_csv(r'C:\Users\Pawel\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
#Exclude participant 26 as we know that he is way off with amplitudes in this paradigm.
data_wide_mDNA = data_wide_mDNA[data_wide_mDNA.participant != 'P26']
data_wide_mDNA.describe()

#import unchanged behavioural data
data_be =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\P_Merged_var.csv')
#Exclude participant 26 as we know that he is way off with amplitudes in this paradigm.
data_be = data_be[data_be.participant != 'P26']

#import data for plots with baseline
freqbase_alpha= pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\freq_long_with_baseline.csv')     
#import data for plots with baseline
freqbase_theta= pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\freq_long_with_baseline_theta.csv')     







######################################################
###BEHAVIOURAL########################################
######################################################



#Plot avergae reaction time per block
corr_rt= sns.catplot(x="blocks", y="corr_rt", kind="bar", data=data_long);
corr_rt.set(xlabel='Conditions', ylabel='Correct RTs')
plt.ylim(0.35, None)
plt.show(corr_rt)
#Plot avergae false alarm rate per block
falserate = sns.catplot(x="blocks", y="false_alarm", kind="bar", data=data_long);
falserate.set(xlabel='Conditions', ylabel='False Alarms Rate')
plt.show(falserate)

#Plot counted false alarms per block
sns.countplot(x="false_alarm", hue="blocks", data=data_be)
data_be.describe()
#Plot avergae omission errors rate per block
omrate = sns.catplot(x="blocks", y="om_err", kind="bar", data=data_long);
omrate.set(xlabel='Conditions', ylabel='Omissioin Errors Rate')
plt.show(omrate)
#Plot counted omission errors per block
sns.countplot(x="om_err", hue="blocks", data=data_be)

######################################################
###PHYSIOLOGICAL######################################
######################################################

####Social media and screentime time per participant sorted###

#Distribution
sns.distplot(data_wide_mDNA["screentime_mean"]);

#Sort by desired value
data_wide_mDNA1 = data_wide_mDNA.sort_values(['screentime_mean']).reset_index(drop=True)
data_wide_mDNA2 = data_wide_mDNA.sort_values(['socialmedia_mean']).reset_index(drop=True)

#Plot sorted data
sns.catplot(x="participant", y="screentime_mean", kind="bar", data=data_wide_mDNA1);
sns.catplot(x="participant", y="socialmedia_mean", kind="bar", data=data_wide_mDNA2);

#Plot mDNA data in bins with duration of 1h
mobdna1= sns.distplot(data_wide_mDNA["screentime_mean"]/60, kde=False, rug=False, color='indigo');
mobdna1.set(xlabel='Screen time mean in h/day', ylabel='Participants')
plt.show(mobdna1)


mobdna2 = sns.distplot(data_wide_mDNA["socialmedia_mean"]/60, kde=False, rug=False, color='royalblue');
mobdna2.set(xlabel='Social media mean in h/day', ylabel='Participants')
plt.show(mobdna2)

###Amplitude and latency of P3b per block###

#Plot every participants amplitude in every block
sns.catplot(x="participant", y="target_maxAmp_Pz", hue="blocks", kind="bar", data=data_long);


#Plot avergae amplitude per block
sns.catplot(x="blocks", y="target_maxAmp_Pz", kind="bar", data=data_long);
#Plot avergae latency per block
sns.catplot(x="blocks", y="latency_target_maxAmp_Pz", kind="bar", data=data_long);

###Amplitude and latency of P3a per sound###
#better to visualize it with the actual ERP plot

#Plot avergae amplitude per block
fig = sns.catplot(x="blocks", y="sound_maxAmp_Cz", kind="bar",order=["buzz_block", "neutral_block"], data=data_long);
plt.xlabel("Sounds")
plt.ylabel("Max Amplitude")
#plt.title("P3a Max Amplitude Sounds") # You can comment this line out if you don't need title
plt.show(fig)

#Plot avergae latency per block
fig = sns.catplot(x="blocks", y="sounds_latency_Cz", kind="bar",order=["buzz_block", "neutral_block"], data=data_long);
plt.xlabel("Sounds")
plt.ylabel("Latency")
#plt.title("P3a Latency for Sounds") # You can comment this line out if you don't need title
plt.show(fig)

###Plot the relation of average social media usage with max amplitude in different blocks
##3 regression lines overlapping 

dupa = data_long
dupa = dupa[data_long.participant != 'P22']
dupa = dupa[data_long.participant != 'P24']
dupa = dupa.set_index('participant')


df = dupa[['target_maxAmp_Pz','blocks']]
df1=df.loc[(df.target_maxAmp_Pz.notnull()) & (df['blocks'].isin(['buzz_block']))]
df5=df.loc[(df.target_maxAmp_Pz.notnull()) & (df['blocks'].isin(['nodis_block']))]
df6=df.loc[(df.target_maxAmp_Pz.notnull()) & (df['blocks'].isin(['neutral_block']))]


df2= dupa['socialmedia_mean'].dropna()

df2=pd.DataFrame(df2)

df3 = pd.concat([df1,df2],sort=False, ignore_index=False)

df4 = df1.join(df2, how='outer')
df7 = df5.join(df2, how='outer')
df8 = df6.join(df2, how='outer')

df_forplot = pd.concat([df4,df7,df8],sort=False, ignore_index=False)


sns.lmplot(x="socialmedia_mean", y="target_maxAmp_Pz", hue="blocks", data=df_forplot);


###Plot the relation of average social media usage with latency in different blocks
##3 regression lines overlapping 

dupa = data_long
dupa = dupa[data_long.participant != 'P22']
dupa = dupa[data_long.participant != 'P24']
dupa = dupa.set_index('participant')


df = dupa[['latency_target_maxAmp_Pz','blocks']]
df1=df.loc[(df.latency_target_maxAmp_Pz.notnull()) & (df['blocks'].isin(['buzz_block']))]
df5=df.loc[(df.latency_target_maxAmp_Pz.notnull()) & (df['blocks'].isin(['nodis_block']))]
df6=df.loc[(df.latency_target_maxAmp_Pz.notnull()) & (df['blocks'].isin(['neutral_block']))]


df2= dupa['socialmedia_mean'].dropna()

df2=pd.DataFrame(df2)

df3 = pd.concat([df1,df2],sort=False, ignore_index=False)

df4 = df1.join(df2, how='outer')
df7 = df5.join(df2, how='outer')
df8 = df6.join(df2, how='outer')

df_forplot = pd.concat([df4,df7,df8],sort=False, ignore_index=False)


sns.lmplot(x="socialmedia_mean", y="latency_target_maxAmp_Pz", hue="blocks", data=df_forplot);

###Plot the relation of average social media usage with latency in different blocks
##3 regression lines overlapping 

dupa = data_long
dupa = dupa[data_long.participant != 'P22']
dupa = dupa[data_long.participant != 'P24']
dupa = dupa.set_index('participant')


df = dupa[['sounds_latency_Cz','blocks']]
df1=df.loc[(df.sounds_latency_Cz.notnull()) & (df['blocks'].isin(['buzz_block']))]
df6=df.loc[(df.sounds_latency_Cz.notnull()) & (df['blocks'].isin(['neutral_block']))]


df2= dupa['socialmedia_mean'].dropna()

df2=pd.DataFrame(df2)


df4 = df1.join(df2, how='outer')
df5 = df6.join(df2, how='outer')

df_forplot = pd.concat([df4,df5],sort=False, ignore_index=False)


sns.lmplot(x="socialmedia_mean", y="sounds_latency_Cz", hue="blocks", data=df_forplot);



###Plot the relation of average social media usage with amplitude for different sounds
##3 regression lines overlapping 

dupa = data_long
dupa = dupa[data_long.participant != 'P22']
dupa = dupa[data_long.participant != 'P24']
dupa = dupa.set_index('participant')


df = dupa[['sound_maxAmp_Cz','blocks']]
df1=df.loc[(df.sound_maxAmp_Cz.notnull()) & (df['blocks'].isin(['buzz_block']))]
df6=df.loc[(df.sound_maxAmp_Cz.notnull()) & (df['blocks'].isin(['neutral_block']))]


df2= dupa['socialmedia_mean'].dropna()

df2=pd.DataFrame(df2)


df4 = df1.join(df2, how='outer')
df5 = df6.join(df2, how='outer')

df_forplot_amp = pd.concat([df4,df5],sort=False, ignore_index=False)


sns.lmplot(x="socialmedia_mean", y="sound_maxAmp_Cz", hue="blocks", data=df_forplot_amp);


###Power estimates plots###

#Absolute parietal alpha log mean psd 
sns.catplot(x="blocks", y="parietal_log_psd_alpha_power", kind="bar", data=freqbase_alpha);

#Absolute [Pz] alpha log mean psd  
sns.catplot(x="blocks", y="Pz_psd_log_alpha_power", kind="bar", data=freqbase_alpha);

#Absolute parietal alpha SIMPSON
sns.catplot(x="blocks", y="parietal_abs_alpha_power", kind="bar", data=freqbase_alpha);

#Absolute alpha [Pz] SIMPSON
sns.catplot(x="blocks", y="abs_alpha_powerPz", kind="bar", data=freqbase_alpha);

#Parietal relative alpha power per block
sns.catplot(x="blocks", y="parietal_alpha_rel_power", kind="bar", data=data_long);

#Parietal absolute power with baseline correction per block
sns.catplot(x="blocks", y="parietal_AlphaPowerDecLog", kind="bar", data=data_long);

#Parietal relative alpha power per block [Pz]
sns.catplot(x="blocks", y="alpha_rel_powerPz", kind="bar", data=data_long);

#Parietal absolute power with baseline correction per block [Pz]
sns.catplot(x="blocks", y="AlphaPowerDecLogPz", kind="bar", data=data_long);



#Absolute frontal theta log mean psd 
sns.catplot(x="blocks", y="frontal_log_psd_theta_power", kind="bar", data=freqbase_theta);

#Absolute [Fz] theta log mean psd  
sns.catplot(x="blocks", y="Fz_psd_log_theta_power", kind="bar", data=freqbase_theta);

#Absolute frontal theta SIMPSON
sns.catplot(x="blocks", y="frontal_abs_theta_power", kind="bar", data=freqbase_theta);

#Absolute theta [Fz] SIMPSON
sns.catplot(x="blocks", y="abs_theta_powerFz", kind="bar", data=freqbase_theta);

#frontal relative theta power per block
sns.catplot(x="blocks", y="frontal_theta_rel_power", kind="bar", data=data_long);

#frontal absolute power with baseline correction per block
sns.catplot(x="blocks", y="frontal_thetaPowerDecLog", kind="bar", data=data_long);

#frontal absolute LOG psd power with baseline correction per block
sns.catplot(x="blocks", y="frontal_declog_psd_theta_power", kind="bar", data=data_long);

#frontal relative theta power per block [Fz]
sns.catplot(x="blocks", y="theta_rel_powerFz", kind="bar", data=data_long);

#frontal absolute power with baseline correction per block [Fz]
sns.catplot(x="blocks", y="thetaPowerDecLogFz", kind="bar", data=data_long);


