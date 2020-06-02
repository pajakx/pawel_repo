# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 12:04:47 2020
 _____ _        _   _     _   _          
/  ___| |      | | (_)   | | (_)         
\ `--.| |_ __ _| |_ _ ___| |_ _  ___ ___ 
 `--. \ __/ _` | __| / __| __| |/ __/ __|
/\__/ / || (_| | |_| \__ \ |_| | (__\__ \
\____/ \__\__,_|\__|_|___/\__|_|\___|___/
                                         
                                         
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
#Exclude participant 26 for ERP analysis as we know that he is way off with amplitudes in this paradigm.
data_long = data_long[data_long.participant != 'P26']
data_long.describe()


data_wide_mDNA =pd.read_csv(r'C:\Users\Pawel\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
#Exclude participant 26 for ERP analysis as we know that he is way off with amplitudes in this paradigm.
data_wide_mDNA = data_wide_mDNA[data_wide_mDNA.participant != 'P26']
data_wide_mDNA.describe()

#Check mobileDNA data distribution

#for screentime
#Use Shapiro test to be sure that distribution is normal

screen_normal =stats.shapiro(data_wide_mDNA['screentime_mean'])

print(screen_normal)

#(0.8090910315513611, 0.00019749953935388476)
#Significant, therfore the distribution is not normal


#for socialmedia

social_normal =stats.shapiro(data_wide_mDNA['socialmedia_mean'])

print(social_normal)

#(0.8280704021453857, 0.00043687698780559003)
#Significant, therfore the distribution is not normal


# ANOVA - does correct reaction time differ between blocks?

aov_corr_rt = pg.rm_anova(data=data_long, dv='corr_rt', within= 'blocks', subject='participant', detailed=True)

print(aov_corr_rt)
'''
   Source    SS  DF   MS      F     p-unc    np2    eps
0  blocks  0.00   2  0.0  0.358  0.700787  0.013  0.927
1   Error  0.01  56  0.0      -         -      -      -
N=29
'''
##Not significant##

######## ANOVA - does omission errors differ between blocks?
aov_omission = pg.rm_anova(data=data_long, dv='om_err', within= 'blocks', subject='participant', detailed=True)


print(aov_omission)
'''
Source   SS  DF   MS      F     p-unc    np2   eps
0  blocks  0.0   2  0.0  0.352  0.704856  0.012  0.77
1   Error  0.0  56  0.0      -         -      -     -
N=29

'''

##Not significant##


######## ANOVA - does false alarms differ between blocks?

aov_false_alarm = pg.rm_anova(data=data_long, dv='false_alarm', within= 'blocks', subject='participant', detailed=True)

print(aov_false_alarm)

'''
   Source   SS  DF   MS      F     p-unc   np2    eps
0  blocks  0.0   2  0.0  1.465  0.239802  0.05  0.903
1   Error  0.0  56  0.0      -         -     -      -
N=29
'''

##Not significant##


######## ANOVA - does max amplitudes for P3b for targets differ between blocks?

aov_max_amp_targets = pg.rm_anova(data=data_long, dv='target_maxAmp_Pz', within= 'blocks', subject='participant', detailed=True)

print(aov_max_amp_targets)

'''
   Source       SS  DF      MS     F     p-unc    np2   eps
0  blocks   11.575   2   5.788  0.53  0.591826  0.019  0.95
1   Error  590.050  54  10.927     -         -      -     -
'''

##Not significant##


######## Paired T-test - does max amplitudes per 2 sounds (buzz and neutral) differ?######

#Check the assumptions for the paird t-test
data_wide_mDNA[['Sound_Block_Buzz_maxAmp_Cz','Sound_Block_Neutral_maxAmp_Cz']].describe()
'''
       Sound_Block_Buzz_maxAmp_Cz  Sound_Block_Neutral_maxAmp_Cz
count                   26.000000                      26.000000
mean                    13.889260                      11.761441
std                      6.573770                       4.687876
min                      0.507805                       3.437281
25%                      9.123733                       8.915750
50%                     13.585047                      11.940167
75%                     18.408472                      14.216514
max                     27.761828                      21.154536
'''
#Check for outliers
data_wide_mDNA[['Sound_Block_Buzz_maxAmp_Cz','Sound_Block_Neutral_maxAmp_Cz']].plot(kind='box')
#Check distribuiton for the difference between two scores

data_wide_mDNA['amp_difference'] = data_wide_mDNA['Sound_Block_Buzz_maxAmp_Cz'] - data_wide_mDNA['Sound_Block_Neutral_maxAmp_Cz']

data_wide_mDNA['amp_difference'].plot(kind='hist', title= 'Distribution of Max Amplitude [Cz] for Sounds')

#Use Shapiro test to be sure that distribution is normal

amp_normal =stats.shapiro(data_wide_mDNA['amp_difference'])

print(amp_normal)

##(0.924861490726471, 0.05852052941918373)##
#Not significant, therfore the distribution is normal

#Finally calculate the paired T-test for max amplitudes for sounds [Cz] P3a

sounds_amp_ttest =  stats.ttest_rel(data_wide_mDNA['Sound_Block_Buzz_maxAmp_Cz'], data_wide_mDNA['Sound_Block_Neutral_maxAmp_Cz'])

print(sounds_amp_ttest)

############################################################################
#Ttest_relResult(statistic=2.3865513399941194, pvalue=0.024893406038574498)#
############################################################################

###p<0.05 so the difference is significant###


######## ANOVA - does latencies  for P3b max amplitudes for targets differ between blocks?

aov_latency_targets = pg.rm_anova(data=data_long, dv='latency_target_maxAmp_Pz', within= 'blocks', subject='participant', detailed=True, correction=True)

print(aov_latency_targets)
'''
   Source         SS  DF       MS  ...    eps sphericity W-spher    p-spher
0  blocks    328.881   2  164.440  ...  0.784      False   0.725  0.0152061
1   Error  38504.452  54  713.045  ...      -          -       -          -
'''
##Not significant##

######## Does latencies for P3a max amplitudes for targets differ between sounds buzz and neutral?

#Check the assumptions for the paird t-test
data_wide_mDNA[['Sound_Block_Buzz_latency_Cz','Sound_Block_Neutral_latency_Cz']].describe()


'''
       Sound_Block_Buzz_latency_Cz  Sound_Block_Neutral_latency_Cz
count                    26.000000                       26.000000
mean                    374.153846                      367.038462
std                      54.270944                       64.661878
min                     316.000000                      301.000000
25%                     326.000000                      314.000000
50%                     354.000000                      327.000000
75%                     419.000000                      436.000000
max                     471.000000                      482.000000
'''


#Check for outliers
data_wide_mDNA[['Sound_Block_Buzz_latency_Cz','Sound_Block_Neutral_latency_Cz']].plot(kind='box')
#Check distribuiton for the difference between two scores

data_wide_mDNA['latency_difference'] = data_wide_mDNA['Sound_Block_Buzz_latency_Cz'] - data_wide_mDNA['Sound_Block_Neutral_latency_Cz']

data_wide_mDNA['latency_difference'].plot(kind='hist', title= 'Distribution of Max Amplitude [Cz] for Sounds')

#Use Shapiro test to be sure that distribution is normal

amp_normal =stats.shapiro(data_wide_mDNA['latency_difference'])

print(amp_normal)

######(0.9446800947189331, 0.17365552484989166)#########
##  p<0.05  The data is normally distribuited #####

#Finally calculate the paired T-test for max amplitudes for sounds [Cz] P3a

sounds_latency_ttest =  stats.ttest_rel(data_wide_mDNA['Sound_Block_Buzz_latency_Cz'], data_wide_mDNA['Sound_Block_Neutral_latency_Cz'])

print(sounds_latency_ttest)

############################################################################
#Ttest_relResult(statistic=0.5046056688542144, pvalue=0.6182548009975886)#
############################################################################

###p>0.05 so the difference is not significant###



##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to average RT correct in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["nodis_block_mean_rt"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                             OLS Regression Results                            
===============================================================================
Dep. Variable:     nodis_block_mean_rt   R-squared:                       0.005
Model:                             OLS   Adj. R-squared:                 -0.036
Method:                  Least Squares   F-statistic:                    0.1317
Date:                 Fri, 28 Feb 2020   Prob (F-statistic):              0.720
Time:                         12:45:13   Log-Likelihood:                 46.564
No. Observations:                   26   AIC:                            -89.13
Df Residuals:                       24   BIC:                            -86.61
Df Model:                            1                                         
Covariance Type:             nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const               0.4134      0.014     30.199      0.000       0.385       0.442
screentime_mean  2.081e-05   5.73e-05      0.363      0.720   -9.75e-05       0.000
==============================================================================
Omnibus:                        8.275   Durbin-Watson:                   2.252
Prob(Omnibus):                  0.016   Jarque-Bera (JB):                6.612
Skew:                           1.193   Prob(JB):                       0.0367
Kurtosis:                       3.640   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to omission error rate in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["nodis_block_mean_omission"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                OLS Regression Results                               
=====================================================================================
Dep. Variable:     nodis_block_mean_omission   R-squared:                       0.000
Model:                                   OLS   Adj. R-squared:                 -0.042
Method:                        Least Squares   F-statistic:                 0.0001636
Date:                       Fri, 28 Feb 2020   Prob (F-statistic):              0.990
Time:                               12:45:34   Log-Likelihood:                 119.75
No. Observations:                         26   AIC:                            -235.5
Df Residuals:                             24   BIC:                            -233.0
Df Model:                                  1                                         
Covariance Type:                   nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const               0.0020      0.001      2.429      0.023       0.000       0.004
screentime_mean  4.395e-08   3.44e-06      0.013      0.990   -7.05e-06    7.13e-06
==============================================================================
Omnibus:                        7.780   Durbin-Watson:                   2.316
Prob(Omnibus):                  0.020   Jarque-Bera (JB):                6.243
Skew:                           1.175   Prob(JB):                       0.0441
Kurtosis:                       3.492   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""
##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to false alarms rate in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["nodis_block_mean_falsAlarm"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                OLS Regression Results                                
======================================================================================
Dep. Variable:     nodis_block_mean_falsAlarm   R-squared:                       0.000
Model:                                    OLS   Adj. R-squared:                 -0.042
Method:                         Least Squares   F-statistic:                 0.0002227
Date:                        Fri, 28 Feb 2020   Prob (F-statistic):              0.988
Time:                                12:45:56   Log-Likelihood:                 120.24
No. Observations:                          26   AIC:                            -236.5
Df Residuals:                              24   BIC:                            -234.0
Df Model:                                   1                                         
Covariance Type:                    nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const               0.0015      0.001      1.899      0.070      -0.000       0.003
screentime_mean  5.032e-08   3.37e-06      0.015      0.988   -6.91e-06    7.01e-06
==============================================================================
Omnibus:                       23.120   Durbin-Watson:                   2.648
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               33.771
Skew:                           1.976   Prob(JB):                     4.64e-08
Kurtosis:                       6.944   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3b amplitude in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Nodis_maxAmp_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                 OLS Regression Results                                 
========================================================================================
Dep. Variable:     Target_Block_Nodis_maxAmp_Pz   R-squared:                       0.175
Model:                                      OLS   Adj. R-squared:                  0.140
Method:                           Least Squares   F-statistic:                     5.076
Date:                          Fri, 28 Feb 2020   Prob (F-statistic):             0.0337
Time:                                  12:46:20   Log-Likelihood:                -77.669
No. Observations:                            26   AIC:                             159.3
Df Residuals:                                24   BIC:                             161.9
Df Model:                                     1                                         
Covariance Type:                      nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const              19.1978      1.628     11.796      0.000      15.839      22.557
screentime_mean    -0.0154      0.007     -2.253      0.034**    -0.029      -0.001
==============================================================================
Omnibus:                        1.609   Durbin-Watson:                   1.556
Prob(Omnibus):                  0.447   Jarque-Bera (JB):                0.992
Skew:                          -0.031   Prob(JB):                        0.609
Kurtosis:                       2.045   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""
########################################################################################
##Significant result means that when average screentime increases by 1 the amplitude####
#decreases by-0.0154  p=0.034 !!                                                    ####
########################################################################################


ax = sns.regplot(x=X, y=y, data=data_wide_mDNA)

##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3b latency in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Nodis_latency_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                 
=========================================================================================
Dep. Variable:     Target_Block_Nodis_latency_Pz   R-squared:                       0.000
Model:                                       OLS   Adj. R-squared:                 -0.041
Method:                            Least Squares   F-statistic:                  0.009133
Date:                           Fri, 28 Feb 2020   Prob (F-statistic):              0.925
Time:                                   12:47:23   Log-Likelihood:                -136.56
No. Observations:                             26   AIC:                             277.1
Df Residuals:                                 24   BIC:                             279.6
Df Model:                                      1                                         
Covariance Type:                       nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const             430.6577     15.673     27.478      0.000     398.311     463.005
screentime_mean    -0.0063      0.066     -0.096      0.925      -0.142       0.129
==============================================================================
Omnibus:                       11.196   Durbin-Watson:                   2.245
Prob(Omnibus):                  0.004   Jarque-Bera (JB):                9.608
Skew:                           1.338   Prob(JB):                      0.00820
Kurtosis:                       4.307   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3b amplitude in smartphone distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Buzz_maxAmp_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                 OLS Regression Results                                
=======================================================================================
Dep. Variable:     Target_Block_Buzz_maxAmp_Pz   R-squared:                       0.118
Model:                                     OLS   Adj. R-squared:                  0.081
Method:                          Least Squares   F-statistic:                     3.210
Date:                         Fri, 28 Feb 2020   Prob (F-statistic):             0.0858
Time:                                 12:47:47   Log-Likelihood:                -80.914
No. Observations:                           26   AIC:                             165.8
Df Residuals:                               24   BIC:                             168.3
Df Model:                                    1                                         
Covariance Type:                     nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const              18.7350      1.844     10.161      0.000      14.929      22.541
screentime_mean    -0.0138      0.008     -1.792      0.086      -0.030       0.002
==============================================================================
Omnibus:                        2.962   Durbin-Watson:                   2.096
Prob(Omnibus):                  0.227   Jarque-Bera (JB):                1.923
Skew:                           0.663   Prob(JB):                        0.382
Kurtosis:                       3.138   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""



##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3b latency in  smartphone distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Buzz_latency_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                 OLS Regression Results                                 
========================================================================================
Dep. Variable:     Target_Block_Buzz_latency_Pz   R-squared:                       0.029
Model:                                      OLS   Adj. R-squared:                 -0.012
Method:                           Least Squares   F-statistic:                    0.7126
Date:                          Fri, 28 Feb 2020   Prob (F-statistic):              0.407
Time:                                  12:48:03   Log-Likelihood:                -137.05
No. Observations:                            26   AIC:                             278.1
Df Residuals:                                24   BIC:                             280.6
Df Model:                                     1                                         
Covariance Type:                      nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const             417.6163     15.973     26.144      0.000     384.649     450.584
screentime_mean     0.0565      0.067      0.844      0.407      -0.082       0.195
==============================================================================
Omnibus:                        7.831   Durbin-Watson:                   1.957
Prob(Omnibus):                  0.020   Jarque-Bera (JB):                6.411
Skew:                           1.198   Prob(JB):                       0.0405
Kurtosis:                       3.417   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3b amplitude in neutral distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Neutral_maxAmp_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                  
==========================================================================================
Dep. Variable:     Target_Block_Neutral_maxAmp_Pz   R-squared:                       0.273
Model:                                        OLS   Adj. R-squared:                  0.242
Method:                             Least Squares   F-statistic:                     9.002
Date:                            Fri, 28 Feb 2020   Prob (F-statistic):            0.00620
Time:                                    12:48:26   Log-Likelihood:                -78.322
No. Observations:                              26   AIC:                             160.6
Df Residuals:                                  24   BIC:                             163.2
Df Model:                                       1                                         
Covariance Type:                        nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const              19.2210      1.669     11.517      0.000      15.777      22.665
screentime_mean    -0.0210      0.007     -3.000      0.006**    -0.035      -0.007
==============================================================================
Omnibus:                        3.061   Durbin-Watson:                   2.232
Prob(Omnibus):                  0.216   Jarque-Bera (JB):                2.162
Skew:                           0.531   Prob(JB):                        0.339
Kurtosis:                       2.069   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##P<0.05 the effect is significant

ax = sns.regplot(x=X, y=y, data=data_wide_mDNA)


##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3b latency in neutral distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Neutral_latency_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                   OLS Regression Results                                  
===========================================================================================
Dep. Variable:     Target_Block_Neutral_latency_Pz   R-squared:                       0.001
Model:                                         OLS   Adj. R-squared:                 -0.041
Method:                              Least Squares   F-statistic:                   0.02071
Date:                             Fri, 28 Feb 2020   Prob (F-statistic):              0.887
Time:                                     12:49:45   Log-Likelihood:                -134.74
No. Observations:                               26   AIC:                             273.5
Df Residuals:                                   24   BIC:                             276.0
Df Model:                                        1                                         
Covariance Type:                         nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const             429.1027     14.615     29.360      0.000     398.939     459.267
screentime_mean    -0.0088      0.061     -0.144      0.887      -0.135       0.118
==============================================================================
Omnibus:                       15.365   Durbin-Watson:                   1.945
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               16.386
Skew:                           1.467   Prob(JB):                     0.000277
Kurtosis:                       5.552   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""



##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3a amplitude in response to vibration sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Buzz_maxAmp_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                OLS Regression Results                                
======================================================================================
Dep. Variable:     Sound_Block_Buzz_maxAmp_Cz   R-squared:                       0.046
Model:                                    OLS   Adj. R-squared:                  0.007
Method:                         Least Squares   F-statistic:                     1.167
Date:                        Fri, 28 Feb 2020   Prob (F-statistic):              0.291
Time:                                12:50:08   Log-Likelihood:                -84.726
No. Observations:                          26   AIC:                             173.5
Df Residuals:                              24   BIC:                             176.0
Df Model:                                   1                                         
Covariance Type:                    nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const              15.7312      2.135      7.368      0.000      11.325      20.138
screentime_mean    -0.0097      0.009     -1.080      0.291      -0.028       0.009
==============================================================================
Omnibus:                        0.462   Durbin-Watson:                   1.446
Prob(Omnibus):                  0.794   Jarque-Bera (JB):                0.582
Skew:                           0.131   Prob(JB):                        0.747
Kurtosis:                       2.315   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3a amplitude in response to neutral sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Neutral_maxAmp_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                 
=========================================================================================
Dep. Variable:     Sound_Block_Neutral_maxAmp_Cz   R-squared:                       0.005
Model:                                       OLS   Adj. R-squared:                 -0.037
Method:                            Least Squares   F-statistic:                    0.1151
Date:                           Fri, 28 Feb 2020   Prob (F-statistic):              0.737
Time:                                   12:50:54   Log-Likelihood:                -76.490
No. Observations:                             26   AIC:                             157.0
Df Residuals:                                 24   BIC:                             159.5
Df Model:                                      1                                         
Covariance Type:                       nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const              12.1828      1.555      7.833      0.000       8.973      15.393
screentime_mean    -0.0022      0.007     -0.339      0.737      -0.016       0.011
==============================================================================
Omnibus:                        0.195   Durbin-Watson:                   2.020
Prob(Omnibus):                  0.907   Jarque-Bera (JB):                0.321
Skew:                           0.176   Prob(JB):                        0.852
Kurtosis:                       2.585   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3a latency in response to vibration sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Buzz_latency_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                 OLS Regression Results                                
=======================================================================================
Dep. Variable:     Sound_Block_Buzz_latency_Cz   R-squared:                       0.139
Model:                                     OLS   Adj. R-squared:                  0.104
Method:                          Least Squares   F-statistic:                     3.891
Date:                         Fri, 28 Feb 2020   Prob (F-statistic):             0.0602
Time:                                 12:51:17   Log-Likelihood:                -138.27
No. Observations:                           26   AIC:                             280.5
Df Residuals:                               24   BIC:                             283.1
Df Model:                                    1                                         
Covariance Type:                     nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const             347.7796     16.743     20.771      0.000     313.223     382.336
screentime_mean     0.1383      0.070      1.972      0.060      -0.006       0.283
==============================================================================
Omnibus:                        1.747   Durbin-Watson:                   2.511
Prob(Omnibus):                  0.418   Jarque-Bera (JB):                1.554
Skew:                           0.499   Prob(JB):                        0.460
Kurtosis:                       2.337   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time (in minutes) on a smartphone per day 
#realtes to max P3a latency in response to neutral sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["screentime_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Neutral_latency_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                  
==========================================================================================
Dep. Variable:     Sound_Block_Neutral_latency_Cz   R-squared:                       0.102
Model:                                        OLS   Adj. R-squared:                  0.065
Method:                             Least Squares   F-statistic:                     2.725
Date:                            Fri, 28 Feb 2020   Prob (F-statistic):              0.112
Time:                                    12:51:53   Log-Likelihood:                -143.38
No. Observations:                              26   AIC:                             290.8
Df Residuals:                                  24   BIC:                             293.3
Df Model:                                       1                                         
Covariance Type:                        nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const             340.1728     20.379     16.692      0.000     298.112     382.234
screentime_mean     0.1409      0.085      1.651      0.112      -0.035       0.317
==============================================================================
Omnibus:                        6.449   Durbin-Watson:                   2.049
Prob(Omnibus):                  0.040   Jarque-Bera (JB):                1.911
Skew:                           0.114   Prob(JB):                        0.385
Kurtosis:                       1.692   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to average RT correct in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["nodis_block_mean_rt"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                             OLS Regression Results                            
===============================================================================
Dep. Variable:     nodis_block_mean_rt   R-squared:                       0.014
Model:                             OLS   Adj. R-squared:                 -0.027
Method:                  Least Squares   F-statistic:                    0.3470
Date:                 Mon, 24 Feb 2020   Prob (F-statistic):              0.561
Time:                         10:52:55   Log-Likelihood:                 46.679
No. Observations:                   26   AIC:                            -89.36
Df Residuals:                       24   BIC:                            -86.84
Df Model:                            1                                         
Covariance Type:             nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                0.4225      0.012     35.499      0.000       0.398       0.447
socialmedia_mean -5.631e-05   9.56e-05     -0.589      0.561      -0.000       0.000
==============================================================================
Omnibus:                        4.700   Durbin-Watson:                   2.029
Prob(Omnibus):                  0.095   Jarque-Bera (JB):                3.582
Skew:                           0.908   Prob(JB):                        0.167
Kurtosis:                       3.079   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""



##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to omission error rate in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["nodis_block_mean_omission"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()


"""
                                OLS Regression Results                               
=====================================================================================
Dep. Variable:     nodis_block_mean_omission   R-squared:                       0.019
Model:                                   OLS   Adj. R-squared:                 -0.022
Method:                        Least Squares   F-statistic:                    0.4661
Date:                       Mon, 24 Feb 2020   Prob (F-statistic):              0.501
Time:                               10:53:20   Log-Likelihood:                 120.00
No. Observations:                         26   AIC:                            -236.0
Df Residuals:                             24   BIC:                            -233.5
Df Model:                                  1                                         
Covariance Type:                   nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                0.0016      0.001      2.325      0.029       0.000       0.003
socialmedia_mean  3.889e-06    5.7e-06      0.683      0.501   -7.87e-06    1.56e-05
==============================================================================
Omnibus:                        8.310   Durbin-Watson:                   2.161
Prob(Omnibus):                  0.016   Jarque-Bera (JB):                6.716
Skew:                           1.209   Prob(JB):                       0.0348
Kurtosis:                       3.591   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to false alarms rate in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["nodis_block_mean_falsAlarm"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                OLS Regression Results                                
======================================================================================
Dep. Variable:     nodis_block_mean_falsAlarm   R-squared:                       0.002
Model:                                    OLS   Adj. R-squared:                 -0.039
Method:                         Least Squares   F-statistic:                   0.05363
Date:                        Mon, 24 Feb 2020   Prob (F-statistic):              0.819
Time:                                10:53:39   Log-Likelihood:                 120.27
No. Observations:                          26   AIC:                            -236.5
Df Residuals:                              24   BIC:                            -234.0
Df Model:                                   1                                         
Covariance Type:                    nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                0.0014      0.001      2.023      0.054   -2.85e-05       0.003
socialmedia_mean  1.306e-06   5.64e-06      0.232      0.819   -1.03e-05    1.29e-05
==============================================================================
Omnibus:                       23.989   Durbin-Watson:                   2.611
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               36.269
Skew:                           2.032   Prob(JB):                     1.33e-08
Kurtosis:                       7.118   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


##Caluculate if spending more average time on social media(in minutes) on a smartphone per day 
#realtes to max P3b amplitude in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Nodis_maxAmp_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()


"""
                                 OLS Regression Results                                 
========================================================================================
Dep. Variable:     Target_Block_Nodis_maxAmp_Pz   R-squared:                       0.139
Model:                                      OLS   Adj. R-squared:                  0.103
Method:                           Least Squares   F-statistic:                     3.882
Date:                          Fri, 28 Feb 2020   Prob (F-statistic):             0.0604
Time:                                  12:52:47   Log-Likelihood:                -78.214
No. Observations:                            26   AIC:                             160.4
Df Residuals:                                24   BIC:                             162.9
Df Model:                                     1                                         
Covariance Type:                      nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const               18.3412      1.451     12.638      0.000      15.346      21.336
socialmedia_mean    -0.0230      0.012     -1.970      0.060      -0.047       0.001
==============================================================================
Omnibus:                        1.973   Durbin-Watson:                   1.472
Prob(Omnibus):                  0.373   Jarque-Bera (JB):                1.194
Skew:                           0.197   Prob(JB):                        0.550
Kurtosis:                       2.027   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


ax = sns.regplot(x=X, y=y, data=data_wide_mDNA)


##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3b latency in nodistractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Nodis_latency_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                 
=========================================================================================
Dep. Variable:     Target_Block_Nodis_latency_Pz   R-squared:                       0.009
Model:                                       OLS   Adj. R-squared:                 -0.032
Method:                            Least Squares   F-statistic:                    0.2135
Date:                           Fri, 28 Feb 2020   Prob (F-statistic):              0.648
Time:                                   12:53:22   Log-Likelihood:                -136.45
No. Observations:                             26   AIC:                             276.9
Df Residuals:                                 24   BIC:                             279.4
Df Model:                                      1                                         
Covariance Type:                       nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const              424.8989     13.628     31.179      0.000     396.773     453.025
socialmedia_mean     0.0506      0.109      0.462      0.648      -0.175       0.276
==============================================================================
Omnibus:                       11.837   Durbin-Watson:                   2.214
Prob(Omnibus):                  0.003   Jarque-Bera (JB):               10.411
Skew:                           1.392   Prob(JB):                      0.00549
Kurtosis:                       4.366   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""



##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3b amplitude in smartphone distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Buzz_maxAmp_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()


#######################
"""
                                 OLS Regression Results                                
=======================================================================================
Dep. Variable:     Target_Block_Buzz_maxAmp_Pz   R-squared:                       0.243
Model:                                     OLS   Adj. R-squared:                  0.212
Method:                          Least Squares   F-statistic:                     7.721
Date:                         Fri, 28 Feb 2020   Prob (F-statistic):             0.0104
Time:                                 12:53:40   Log-Likelihood:                -78.920
No. Observations:                           26   AIC:                             161.8
Df Residuals:                               24   BIC:                             164.4
Df Model:                                    1                                         
Covariance Type:                     nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const               19.0988      1.491     12.808      0.000      16.021      22.176
socialmedia_mean    -0.0333      0.012     -2.779      0.010**    -0.058      -0.009
==============================================================================
Omnibus:                        2.878   Durbin-Watson:                   1.985
Prob(Omnibus):                  0.237   Jarque-Bera (JB):                2.180
Skew:                           0.706   Prob(JB):                        0.336
Kurtosis:                       2.865   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""
#########################
#p<0.05 the effect is significant 
ax = sns.regplot(x=X, y=y, data=data_wide_mDNA)



##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3b latency in  smartphone distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Buzz_latency_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                 OLS Regression Results                                 
========================================================================================
Dep. Variable:     Target_Block_Buzz_latency_Pz   R-squared:                       0.021
Model:                                      OLS   Adj. R-squared:                 -0.020
Method:                           Least Squares   F-statistic:                    0.5115
Date:                          Fri, 28 Feb 2020   Prob (F-statistic):              0.481
Time:                                  12:54:23   Log-Likelihood:                -137.16
No. Observations:                            26   AIC:                             278.3
Df Residuals:                                24   BIC:                             280.8
Df Model:                                     1                                         
Covariance Type:                      nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const              421.1276     14.005     30.070      0.000     392.223     450.033
socialmedia_mean     0.0804      0.112      0.715      0.481      -0.152       0.313
==============================================================================
Omnibus:                        6.405   Durbin-Watson:                   1.913
Prob(Omnibus):                  0.041   Jarque-Bera (JB):                5.287
Skew:                           1.103   Prob(JB):                       0.0711
Kurtosis:                       3.114   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3b amplitude in neutral distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Neutral_maxAmp_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                  
==========================================================================================
Dep. Variable:     Target_Block_Neutral_maxAmp_Pz   R-squared:                       0.117
Model:                                        OLS   Adj. R-squared:                  0.080
Method:                             Least Squares   F-statistic:                     3.167
Date:                            Fri, 28 Feb 2020   Prob (F-statistic):             0.0878
Time:                                    12:54:54   Log-Likelihood:                -80.851
No. Observations:                              26   AIC:                             165.7
Df Residuals:                                  24   BIC:                             168.2
Df Model:                                       1                                         
Covariance Type:                        nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const               17.2932      1.606     10.767      0.000      13.978      20.608
socialmedia_mean    -0.0230      0.013     -1.780      0.088      -0.050       0.004
==============================================================================
Omnibus:                        0.818   Durbin-Watson:                   2.183
Prob(Omnibus):                  0.664   Jarque-Bera (JB):                0.796
Skew:                           0.205   Prob(JB):                        0.672
Kurtosis:                       2.247   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

ax = sns.regplot(x=X, y=y, data=data_wide_mDNA)


##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3b latency in neutral distractor condition

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Target_Block_Neutral_latency_Pz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                   OLS Regression Results                                  
===========================================================================================
Dep. Variable:     Target_Block_Neutral_latency_Pz   R-squared:                       0.026
Model:                                         OLS   Adj. R-squared:                 -0.014
Method:                              Least Squares   F-statistic:                    0.6519
Date:                             Fri, 28 Feb 2020   Prob (F-statistic):              0.427
Time:                                     12:55:18   Log-Likelihood:                -134.40
No. Observations:                               26   AIC:                             272.8
Df Residuals:                                   24   BIC:                             275.3
Df Model:                                        1                                         
Covariance Type:                         nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const              434.7925     12.597     34.514      0.000     408.793     460.792
socialmedia_mean    -0.0817      0.101     -0.807      0.427      -0.290       0.127
==============================================================================
Omnibus:                       12.480   Durbin-Watson:                   1.994
Prob(Omnibus):                  0.002   Jarque-Bera (JB):               11.689
Skew:                           1.280   Prob(JB):                      0.00290
Kurtosis:                       5.058   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3a amplitude in response to vibration sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Buzz_maxAmp_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                OLS Regression Results                                
======================================================================================
Dep. Variable:     Sound_Block_Buzz_maxAmp_Cz   R-squared:                       0.039
Model:                                    OLS   Adj. R-squared:                 -0.001
Method:                         Least Squares   F-statistic:                    0.9769
Date:                        Fri, 28 Feb 2020   Prob (F-statistic):              0.333
Time:                                12:57:16   Log-Likelihood:                -84.824
No. Observations:                          26   AIC:                             173.6
Df Residuals:                              24   BIC:                             176.2
Df Model:                                   1                                         
Covariance Type:                    nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const               15.2294      1.871      8.138      0.000      11.367      19.092
socialmedia_mean    -0.0149      0.015     -0.988      0.333      -0.046       0.016
==============================================================================
Omnibus:                        0.971   Durbin-Watson:                   1.400
Prob(Omnibus):                  0.615   Jarque-Bera (JB):                0.940
Skew:                           0.303   Prob(JB):                        0.625
Kurtosis:                       2.292   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""



##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3a latency in response to a smartphone sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Buzz_latency_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                 OLS Regression Results                                
=======================================================================================
Dep. Variable:     Sound_Block_Buzz_latency_Cz   R-squared:                       0.191
Model:                                     OLS   Adj. R-squared:                  0.158
Method:                          Least Squares   F-statistic:                     5.680
Date:                         Fri, 28 Feb 2020   Prob (F-statistic):             0.0254
Time:                                 12:57:46   Log-Likelihood:                -137.46
No. Observations:                           26   AIC:                             278.9
Df Residuals:                               24   BIC:                             281.4
Df Model:                                    1                                         
Covariance Type:                     nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const              349.6814     14.173     24.673      0.000     320.431     378.932
socialmedia_mean     0.2713      0.114      2.383      0.025**     0.036       0.506
==============================================================================
Omnibus:                        1.396   Durbin-Watson:                   2.009
Prob(Omnibus):                  0.498   Jarque-Bera (JB):                1.292
Skew:                           0.454   Prob(JB):                        0.524
Kurtosis:                       2.392   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

###p<0.05 the effect is significant
ax = sns.regplot(x=X, y=y, data=data_wide_mDNA)


########################################################################################
##Significant result means that when average social media screentime increases by 1 ####
##the latency increases by 0.2680   p=0.025!!                                       ####
########################################################################################


##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3a amplitude in response to neutral sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Neutral_maxAmp_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                 
=========================================================================================
Dep. Variable:     Sound_Block_Neutral_maxAmp_Cz   R-squared:                       0.001
Model:                                       OLS   Adj. R-squared:                 -0.041
Method:                            Least Squares   F-statistic:                   0.01229
Date:                           Fri, 28 Feb 2020   Prob (F-statistic):              0.913
Time:                                   12:58:16   Log-Likelihood:                -76.545
No. Observations:                             26   AIC:                             157.1
Df Residuals:                                 24   BIC:                             159.6
Df Model:                                      1                                         
Covariance Type:                       nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const               11.8708      1.361      8.722      0.000       9.062      14.680
socialmedia_mean    -0.0012      0.011     -0.111      0.913      -0.024       0.021
==============================================================================
Omnibus:                        0.353   Durbin-Watson:                   2.033
Prob(Omnibus):                  0.838   Jarque-Bera (JB):                0.452
Skew:                           0.237   Prob(JB):                        0.798
Kurtosis:                       2.561   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#realtes to max P3a latency in response to neutral sound

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["Sound_Block_Neutral_latency_Cz"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                  
==========================================================================================
Dep. Variable:     Sound_Block_Neutral_latency_Cz   R-squared:                       0.225
Model:                                        OLS   Adj. R-squared:                  0.193
Method:                             Least Squares   F-statistic:                     6.962
Date:                            Fri, 28 Feb 2020   Prob (F-statistic):             0.0144
Time:                                    12:58:32   Log-Likelihood:                -141.47
No. Observations:                              26   AIC:                             286.9
Df Residuals:                                  24   BIC:                             289.5
Df Model:                                       1                                         
Covariance Type:                        nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const              335.4326     16.533     20.289      0.000     301.311     369.555
socialmedia_mean     0.3503      0.133      2.639      0.014**     0.076       0.624
==============================================================================
Omnibus:                        3.361   Durbin-Watson:                   2.340
Prob(Omnibus):                  0.186   Jarque-Bera (JB):                1.649
Skew:                           0.285   Prob(JB):                        0.439
Kurtosis:                       1.905   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""
########################################################################################
##Significant result means that when average social media screentime increases by 1 ####
##the latency increases by 0.3503   p= 0.014!                                      ####
########################################################################################

###p<0.05 the effect is significant


ax = sns.regplot(x=X, y=y, data=data_wide_mDNA)


####Regression to see all the target amplitudes combined predicted by average time
##spent on social media
dupa = data_long
dupa = dupa[data_long.participant != 'P22']
dupa = dupa[data_long.participant != 'P24']
dupa = dupa.set_index('participant')


X = dupa["socialmedia_mean"].dropna() ## X usually means our input variables (or independent variables)
y = dupa["target_maxAmp_Pz"].dropna() ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

X1=X
X2=X
X= X.append(X1) 
X =X.append(X2)
X=X.sort_index()

y=y.sort_index()

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)
# Print out the statistics
model.summary()

"""
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       target_maxAmp_Pz   R-squared:                       0.162
Model:                            OLS   Adj. R-squared:                  0.151
Method:                 Least Squares   F-statistic:                     14.64
Date:                Fri, 28 Feb 2020   Prob (F-statistic):           0.000265
Time:                        13:00:18   Log-Likelihood:                -238.70
No. Observations:                  78   AIC:                             481.4
Df Residuals:                      76   BIC:                             486.1
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const               18.2444      0.859     21.238      0.000      16.533      19.955
socialmedia_mean    -0.0264      0.007     -3.826      0.000**    -0.040      -0.013
==============================================================================
Omnibus:                        2.562   Durbin-Watson:                   1.182
Prob(Omnibus):                  0.278   Jarque-Bera (JB):                2.470
Skew:                           0.372   Prob(JB):                        0.291
Kurtosis:                       2.544   Cond. No.                         181.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


ax = sns.regplot(x=X, y=y, data=dupa)

####Regression to see all the target amplitudes combined predicted by average time
##spent on smartphone (SCREENTIME)
dupa = data_long
dupa = dupa[data_long.participant != 'P22']
dupa = dupa[data_long.participant != 'P24']
dupa = dupa.set_index('participant')


X = dupa["screentime_mean"].dropna() ## X usually means our input variables (or independent variables)
y = dupa["target_maxAmp_Pz"].dropna() ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

X1=X
X2=X
X= X.append(X1) 
X =X.append(X2)
X=X.sort_index()

y=y.sort_index()

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)
# Print out the statistics
model.summary()

"""
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       target_maxAmp_Pz   R-squared:                       0.182
Model:                            OLS   Adj. R-squared:                  0.171
Method:                 Least Squares   F-statistic:                     16.88
Date:                Fri, 28 Feb 2020   Prob (F-statistic):           9.97e-05
Time:                        13:54:33   Log-Likelihood:                -237.75
No. Observations:                  78   AIC:                             479.5
Df Residuals:                      76   BIC:                             484.2
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
const              19.0513      0.972     19.602      0.000      17.116      20.987
screentime_mean    -0.0167      0.004     -4.108      0.000      -0.025      -0.009
==============================================================================
Omnibus:                        3.470   Durbin-Watson:                   1.254
Prob(Omnibus):                  0.176   Jarque-Bera (JB):                3.069
Skew:                           0.395   Prob(JB):                        0.216
Kurtosis:                       2.434   Cond. No.                         397.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""




###Correlation between variables

correlations = data_wide_mDNA.corr()


#########POWER ESITMATES##############



############PARIETAL ALPHA######################






######## ANOVA - does parietal absolute alpha power with baseline correction differ between blocks?

aov_declog = pg.rm_anova(data=data_long, dv='parietal_AlphaPowerDecLog', within= 'blocks', subject='participant', detailed=True,correction=True)

print(aov_declog)

'''
pGGCOrr
0.4296395566817678

'''
###Correlation between variables

correlations = data_wide_mDNA.corr()

######## ANOVA - does parietal absolute alpha power [Pz] with baseline correction differ between blocks?

aov_declogPz = pg.rm_anova(data=data_long, dv='AlphaPowerDecLogPz', within= 'blocks', subject='participant', detailed=True)

print(aov_declogPz)

'''
   Source      SS  DF     MS      F     p-unc    np2    eps
0  blocks   1.389   2  0.695  0.748  0.477865  0.026  0.856
1   Error  51.985  56  0.928      -         -      -      -

'''


######## ANOVA - does parietal relative power differ between blocks?

aov_relpow = pg.rm_anova(data=data_long, dv='parietal_alpha_rel_power', within= 'blocks', subject='participant', detailed=True)

print(aov_relpow)

'''
   Source     SS  DF     MS      F     p-unc    np2    eps
0  blocks  0.003   2  0.001  0.846  0.434332  0.029  0.796
1   Error  0.084  56  0.001      -         -      -      -

'''

######## ANOVA - does parietal relative power [Pz] differ between blocks?

aov_relpowPz = pg.rm_anova(data=data_long, dv='alpha_rel_powerPz', within= 'blocks', subject='participant', detailed=True)

print(aov_relpowPz)

'''
   Source     SS  DF     MS      F     p-unc    np2    eps
0  blocks  0.002   2  0.001  0.822  0.444732  0.029  0.811
1   Error  0.081  56  0.001      -         -      -      -

'''

######## ANOVA - does parietal alpha power psd dec log differ between blocks?

aov_relpowPsd = pg.rm_anova(data=data_long, dv='parietal_declog_psd_alpha_power', within= 'blocks', subject='participant', detailed=True)

print(aov_relpowPsd)

'''
   Source      SS  DF     MS      F  ...    np2    eps sphericity W-spher    p-spher
0  blocks   1.571   2  0.785  0.915  ...  0.032  0.825      False   0.788  0.0401991
1   Error  48.041  56  0.858      -  ...      -      -          -       -          -
'''


##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#relates to parietal absolute alpha power with baseline correction in nodis block

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["parietal_nodis_AlphaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                   OLS Regression Results                                  
===========================================================================================
Dep. Variable:     parietal_nodis_AlphaPowerDecLog   R-squared:                       0.012
Model:                                         OLS   Adj. R-squared:                 -0.028
Method:                              Least Squares   F-statistic:                    0.2971
Date:                             Wed, 04 Mar 2020   Prob (F-statistic):              0.591
Time:                                     15:37:53   Log-Likelihood:                -60.201
No. Observations:                               27   AIC:                             124.4
Df Residuals:                                   25   BIC:                             127.0
Df Model:                                        1                                         
Covariance Type:                         nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                1.2510      0.661      1.893      0.070      -0.110       2.612
socialmedia_mean    -0.0029      0.005     -0.545      0.591      -0.014       0.008
==============================================================================
Omnibus:                        2.261   Durbin-Watson:                   2.490
Prob(Omnibus):                  0.323   Jarque-Bera (JB):                0.986
Skew:                           0.138   Prob(JB):                        0.611
Kurtosis:                       3.894   Cond. No.                         182.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#relates to parietal absolute alpha power with baseline correction in buzz block

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["parietal_buzz_AlphaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                  
==========================================================================================
Dep. Variable:     parietal_buzz_AlphaPowerDecLog   R-squared:                       0.023
Model:                                        OLS   Adj. R-squared:                 -0.016
Method:                             Least Squares   F-statistic:                    0.5913
Date:                            Wed, 04 Mar 2020   Prob (F-statistic):              0.449
Time:                                    15:38:45   Log-Likelihood:                -56.114
No. Observations:                              27   AIC:                             116.2
Df Residuals:                                  25   BIC:                             118.8
Df Model:                                       1                                         
Covariance Type:                        nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                1.0052      0.568      1.770      0.089      -0.165       2.175
socialmedia_mean    -0.0035      0.005     -0.769      0.449      -0.013       0.006
==============================================================================
Omnibus:                        6.764   Durbin-Watson:                   2.165
Prob(Omnibus):                  0.034   Jarque-Bera (JB):                6.300
Skew:                          -0.524   Prob(JB):                       0.0428
Kurtosis:                       5.122   Cond. No.                         182.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#relates to parietal absolute alpha power with baseline correction in neutral block

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["parietal_neutral_AlphaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                    OLS Regression Results                                   
=============================================================================================
Dep. Variable:     parietal_neutral_AlphaPowerDecLog   R-squared:                       0.026
Model:                                           OLS   Adj. R-squared:                 -0.013
Method:                                Least Squares   F-statistic:                    0.6647
Date:                               Wed, 04 Mar 2020   Prob (F-statistic):              0.423
Time:                                       15:39:40   Log-Likelihood:                -59.681
No. Observations:                                 27   AIC:                             123.4
Df Residuals:                                     25   BIC:                             126.0
Df Model:                                          1                                         
Covariance Type:                           nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                1.4500      0.648      2.237      0.034       0.115       2.785
socialmedia_mean    -0.0043      0.005     -0.815      0.423      -0.015       0.007
==============================================================================
Omnibus:                        1.675   Durbin-Watson:                   2.441
Prob(Omnibus):                  0.433   Jarque-Bera (JB):                0.550
Skew:                           0.059   Prob(JB):                        0.760
Kurtosis:                       3.689   Cond. No.                         182.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""









###########FRONTAL THETA POWER#################



######## ANOVA - does parietal absolute alpha power with baseline correction differ between blocks?

aov_declog = pg.rm_anova(data=data_long, dv='frontal_thetaPowerDecLog', within= 'blocks', subject='participant', detailed=True)

print(aov_declog)

'''
   Source      SS  DF     MS    F     p-unc    np2   eps
0  blocks   0.763   2  0.382  0.7  0.500764  0.024  0.99
1   Error  30.522  56  0.545    -         -      -     -

'''


######## ANOVA - does frontal theta  (mean psd) with baseline correction differ between blocks?

aov_declogFz = pg.rm_anova(data=data_long, dv='declog_psd_theta_powerFz', within= 'blocks', subject='participant', detailed=True)

print(aov_declogFz)

'''
   Source      SS  DF     MS      F     p-unc    np2    eps
0  blocks   0.607   2  0.303  0.655  0.523546  0.023  0.978
1   Error  25.953  56  0.463      -         -      -      -

'''


######## ANOVA - does frontal theta relative power differ between blocks?

aov_relpow = pg.rm_anova(data=data_long, dv='frontal_theta_rel_power', within= 'blocks', subject='participant', detailed=True)

print(aov_relpow)

'''
   Source     SS  DF   MS      F    p-unc    np2    eps
0  blocks  0.000   2  0.0  0.612  0.54561  0.021  0.824
1   Error  0.011  56  0.0      -        -      -      -

'''

######## ANOVA - does frontal theta relative power [Fz] differ between blocks?

aov_relpowFz = pg.rm_anova(data=data_long, dv='theta_rel_powerFz', within= 'blocks', subject='participant', detailed=True)

print(aov_relpowFz)

'''
   Source     SS  DF   MS      F     p-unc    np2    eps
0  blocks  0.000   2  0.0  0.645  0.528619  0.023  0.821
1   Error  0.013  56  0.0      -         -      -      -

'''

######## ANOVA - does frontal theta declog psd differ between blocks?

aov_PSDthetafrontal = pg.rm_anova(data=data_long, dv='frontal_declog_psd_theta_power', within= 'blocks', subject='participant', detailed=True)

print(aov_PSDthetafrontal)

'''
   Source      SS  DF     MS      F     p-unc    np2    eps
0  blocks   0.655   2  0.327  0.588  0.558771  0.021  0.987
1   Error  31.162  56  0.556      -         -      -      -

'''

##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#relates to frontal absolute theta power with baseline correction in nodis block

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_nodis_declog_psd_theta_power"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                  
==========================================================================================
Dep. Variable:     frontal_nodis_thetaPowerDecLog   R-squared:                       0.000
Model:                                        OLS   Adj. R-squared:                 -0.039
Method:                             Least Squares   F-statistic:                   0.01244
Date:                            Fri, 06 Mar 2020   Prob (F-statistic):              0.912
Time:                                    12:49:26   Log-Likelihood:                -54.276
No. Observations:                              27   AIC:                             112.6
Df Residuals:                                  25   BIC:                             115.1
Df Model:                                       1                                         
Covariance Type:                        nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                0.9011      0.531      1.698      0.102      -0.192       1.994
socialmedia_mean    -0.0005      0.004     -0.112      0.912      -0.009       0.008
==============================================================================
Omnibus:                        1.636   Durbin-Watson:                   2.562
Prob(Omnibus):                  0.441   Jarque-Bera (JB):                0.992
Skew:                          -0.469   Prob(JB):                        0.609
Kurtosis:                       3.019   Cond. No.                         182.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#relates to parietal absolute alpha power with baseline correction in buzz block

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_buzz_thetaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                  OLS Regression Results                                 
=========================================================================================
Dep. Variable:     frontal_buzz_thetaPowerDecLog   R-squared:                       0.006
Model:                                       OLS   Adj. R-squared:                 -0.034
Method:                            Least Squares   F-statistic:                    0.1565
Date:                           Fri, 06 Mar 2020   Prob (F-statistic):              0.696
Time:                                   12:51:48   Log-Likelihood:                -51.160
No. Observations:                             27   AIC:                             106.3
Df Residuals:                                 25   BIC:                             108.9
Df Model:                                      1                                         
Covariance Type:                       nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                0.9370      0.473      1.982      0.059      -0.037       1.911
socialmedia_mean     0.0015      0.004      0.396      0.696      -0.006       0.009
==============================================================================
Omnibus:                        1.022   Durbin-Watson:                   2.027
Prob(Omnibus):                  0.600   Jarque-Bera (JB):                0.349
Skew:                           0.261   Prob(JB):                        0.840
Kurtosis:                       3.191   Cond. No.                         182.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

##Caluculate if spending more average time on social media (in minutes) on a smartphone per day 
#relates to parietal absolute alpha power with baseline correction in neutral block

###In this equation, Y is the dependent variable — or the variable we are trying to
##predict or estimate; X is the independent variable — the variable we are using to 
#make predictions;

X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_neutral_declog_psd_theta_power"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

"""
                                   OLS Regression Results                                   
============================================================================================
Dep. Variable:     frontal_neutral_thetaPowerDecLog   R-squared:                       0.006
Model:                                          OLS   Adj. R-squared:                 -0.034
Method:                               Least Squares   F-statistic:                    0.1459
Date:                              Fri, 06 Mar 2020   Prob (F-statistic):              0.706
Time:                                      12:52:28   Log-Likelihood:                -55.095
No. Observations:                                27   AIC:                             114.2
Df Residuals:                                    25   BIC:                             116.8
Df Model:                                         1                                         
Covariance Type:                          nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const                1.2356      0.547      2.259      0.033       0.109       2.362
socialmedia_mean    -0.0017      0.004     -0.382      0.706      -0.011       0.007
==============================================================================
Omnibus:                        3.106   Durbin-Watson:                   1.995
Prob(Omnibus):                  0.212   Jarque-Bera (JB):                1.751
Skew:                          -0.216   Prob(JB):                        0.417
Kurtosis:                       4.170   Cond. No.                         182.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""


