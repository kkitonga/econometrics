# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 04:10:51 2022

@author: KKITONGA
Content:VAR model with VARMAX syntax
        forecasting
"""

#===========================LOAD LIBRARIES==============================#
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import seaborn as sns

#==========================LOAD DATA====================================#

#i.Loading data
USMacroG = sm.datasets.get_rdataset('USMacroG',package='AER')
USMacroG = USMacroG.data

#2.descriptives
print( USMacroG.dtypes)
print( USMacroG.head())
print( USMacroG.info())

#3.Subsetting consumption and dpi
#creating training dataset
df= USMacroG[['consumption','dpi']].iloc[0:190]
df_full= USMacroG[['consumption','dpi']].dropna()

#==========================VISUALIZATION==============================#

#1.Line plots:consumption AND disposbale personal income
plt.plot(df.consumption,'b',label='consumption')
plt.plot(df.dpi,'r',label='disposable personal \nincome')
plt.xlabel('observations across time')
plt.ylabel('dpi/expenditure')
plt.legend(loc="upper left")
plt.title('Plot of consumption and dpi across time')
  
#2.acf plots
#consumption
sm.graphics.tsa.plot_acf(df.consumption)
#disposable personal income
sm.graphics.tsa.plot_acf(df.dpi)

#3.Histogram
#i.with histogram
sns.distplot(df['consumption'])
#ii.without histogram
sns.distplot(df['dpi'],hist=False)

#4.Pairplot
sns.pairplot(df_full)

#==================STATISTICAL TEST:STATIONARITY======================#

#1.Adf for consumption
adf_test_consump = sm.tsa.adfuller(df.consumption,maxlag=12)
print("adf test statistic:",adf_test_consump[0],
      "\np-value :",adf_test_consump[1],
      '\nused lags:',adf_test_consump[2],
      '\nno of observations:',adf_test_consump[3])
for key,val in adf_test_consump[4].items():
    print(key,":",val)
          
#2.Adf for dpi
adf_test_dpi = sm.tsa.adfuller(df.dpi,maxlag=12)
print("adf test statistic:",adf_test_dpi[0],
      "\np-value :",adf_test_dpi[1],
      '\nused lags:',adf_test_dpi[2],
      '\nno of observations:',adf_test_dpi[3])
for key,val in adf_test_dpi[4].items():
    print(key,":",val)
    
#==================DIFFERENCING THEN CHECKING STATIONARITY============#

#1.taking first and second diffferences for consumption and dpi
df['consump_diff1'] =  df.consumption.diff()
df['dpi_diff1'] =  df.dpi.diff()
df['consump_diff2'] =  df.consump_diff1.diff()
df['dpi_diff2'] =  df.dpi_diff1.diff()
print(df.head())

#2.adfuller test for differenced variables
#i.adfuller :differenced consumption
adf_test_consump_d1 = sm.tsa.adfuller(df.consumption.diff()[1:])
print("adf test statistic:",adf_test_consump_d1[0],
      "\np-value :",adf_test_consump_d1[1],
      '\nused lags:',adf_test_consump_d1[2],
      '\nno of observations:',adf_test_consump_d1[3])
for key,val in adf_test_consump_d1[4].items():
    print(key,":",val)

#ii.adfuller :differenced dpi
adf_test_dpi_d1 = sm.tsa.adfuller(df.dpi.diff()[1:])
print("adf test statistic:",adf_test_dpi_d1[0],
      "\np-value :",adf_test_dpi_d1[1],
      '\nused lags:',adf_test_dpi_d1[2],
      '\nno of observations:',adf_test_dpi_d1[3])
for key,val in adf_test_dpi_d1[4].items():
    print(key,":",val)
        
    
#================PLOTS:LEVEL VERSES DIFFERENCED DATA=================#

#1.CONSUMPTION
#I.Creating figure size
plt.figure(figsize=(20,8))

#ii.creating first sub-plot
plt.subplot(121)
#plot details for first plot
plt.plot(df_full.consumption,'b')
plt.xlabel('Observations across time',fontsize=20)
plt.ylabel('consumption',fontsize=20)
plt.legend(loc="upper left")
plt.title('Consumption trends:level variable',fontsize=20)

#ii.creating second subplot
plt.subplot(122)
#plot details for second plot
plt.plot(df.consumption.diff()[1:],'b')
plt.xlabel('Observations across time',fontsize=20)
plt.ylabel('differenced consumption',fontsize=20)
plt.legend(loc="upper left")
plt.title('Consumption trends:first difference',fontsize=20)


#2.DPI
#I.Creating figure size
plt.figure(figsize=(20,8))

#ii.creating first sub-plot
plt.subplot(121)
#plot details for first plot
plt.plot(df_full.dpi,'b')
plt.xlabel('Observations across time',fontsize=20)
plt.ylabel('Disposable personal income',fontsize=20)
plt.legend(loc="upper left")
plt.title('DPI trends:level variable',fontsize=20)

#ii.creating second subplot
plt.subplot(122)
#plot details for second plot
plt.plot(df.dpi.diff()[1:],'b')
plt.xlabel('Observations across time',fontsize=20)
plt.ylabel('Differenced dpi',fontsize=20)
plt.legend(loc="upper left")
plt.title('DPI trends:first difference',fontsize=20)


    
#========================GRANGER CAUSALITY===========================#

#1.Granger causality
print('consumption causes dpi')
granger_con_dpi = sm.tsa.stattools.grangercausalitytests(df[['consumption','dpi']], maxlag=4)

print('dpi causes consumption')
granger_dpi_con = sm.tsa.stattools.grangercausalitytests(df[['dpi','consumption']], maxlag=4)

#2.Creating testing and training
df_test = df_full[191:]
df_train = df[['consump_diff1','dpi_diff1']].dropna()
df_train2 = df[['consumption','dpi']].dropna()


#=====================ESTABLISH OPTIMAL LAG===========================#

lag = sm.tsa.VAR(df_train)
select_lag = lag.select_order(maxlags=10)
print(select_lag.summary())

#observations : bic AND hqic=1;AIC and FPE :3

#====================VAR model=======================================#

#1.Var model with 3 lags
#With VARMAX ,there is option ot enforce stationarity 
#on level variables and run VAR model

varmod11 = sm.tsa.VARMAX(df_train2,order=(3,0),enforce_stationarity=True)
varmod11 = varmod11.fit()
print(varmod11.summary())

#2.Var model with 1 lag
varmod22 = sm.tsa.VARMAX(df_train2,order=(1,0),enforce_stationarity=True)
varmod22 = varmod22.fit()
print(varmod22.summary())

#3.Define prediction timeframe
period_predict = 13

#i.prediction with varmo11
predict = varmod11.get_prediction(start=len(df_train2),end=len(df_train2) + period_predict)
predict_mean = predict.predicted_mean
predict_mean = predict_mean.rename(columns={'consumption':'consumption_pred',
                                            'dpi':'dpi_pred'})

#i.prediction with varmo11
predict1 = varmod22.get_prediction(start=len(df_train2),end=len(df_train2) + period_predict)
predict_mean1 = predict1.predicted_mean
predict_mean1 = predict_mean1.rename(columns={'consumption':'consumption_pred_lag1',
                                            'dpi':'dpi_pred_lag1'})

#iii.combine test data plus predicted values using one lag and three lags
observed_predict = pd.concat([df_test,predict_mean1],axis=1)
observed_predict= observed_predict.dropna()
print(observed_predict)


#====================PLOTS:OBSERVED VERSUS PREDICT======================#

#I.Creating figure size
plt.figure(figsize=(20,8))

#ii.creating first sub-plot
plt.subplot(121)
#plot details for first plot
plt.plot(observed_predict.consumption,'b',label='actual consumption')
plt.plot(observed_predict.consumption_pred_lag1 ,'g',label='predicted \nconsumption')
plt.xlabel('Observations across time',fontsize=20)
plt.ylabel('Observed/predicted consumption',fontsize=20)
plt.legend(loc="upper left")
plt.title('Observed versus predicted consumption',fontsize=20)

#ii.creating second subplot
plt.subplot(122)
#plot details for second plot
plt.plot(observed_predict.dpi,'b',label='actual dpi')
plt.plot(observed_predict.consumption_pred_lag1 ,'g',label='predicted \ndpi')
plt.xlabel('Observations across time',fontsize=20)
plt.ylabel('Observed/predicted dpi',fontsize=20)
plt.legend(loc="upper left")
plt.title('Observed versus predicted dpi',fontsize=20)

#=====================END============================================#
