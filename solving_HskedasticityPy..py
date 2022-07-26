# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#===========================LOADING LIBRARIES=================================#

import numpy as np
import statsmodels.api as sm
from statsmodels.compat import lzip


#===========================LOADING DATASET==================================#

#loading CPS1985 data from R datasets
CPS1985 = sm.datasets.get_rdataset("CPS1985",package="AER")

#converting to dataframe
data = CPS1985.data

#===========================REGRESSION========================================#

#1.level model
reg = sm.formula.ols('wage ~ experience + education',data)
reg = reg.fit()
print(reg.summary())

#breusch pagan test:there is heteroskedasticity
bp_test_name = ["lagrange statistic","p-value","f-value","f-statistic"]
bptest = np.round(sm.stats.diagnostic.het_breuschpagan(reg.resid,reg.model.exog),2)
print(dict(lzip(bp_test_name, bptest)))


#====================RESOLVING HETEROSKEDASTICITY=============================#

                       #1.Adjusting functional forms
#i.logging depedent variable
log_reg = sm.formula.ols('np.log(wage) ~ experience + education',data)
log_reg = log_reg.fit()
print(log_reg.summary())

bp_test_name2 = ["lagrange statistic","p-value","f-value","f-statistic"]
bptest2 = np.round(sm.stats.diagnostic.het_breuschpagan(log_reg.resid,log_reg.model.exog),2)
print(dict(lzip(bp_test_name2, bptest2)))


#ii.Logging dependent and independent variable
log_reg2 = sm.formula.ols('np.log(wage) ~ np.log(education) + experience',data)
log_reg2 = log_reg2.fit()
print(log_reg2.summary())

bp_test_name3 = ["lagrange statistic","p-value","f-value","f-statistic"]
bptest3 = np.round(sm.stats.diagnostic.het_breuschpagan(log_reg2.resid,log_reg2.model.exog),2)
print(dict(lzip(bp_test_name3, bptest3)))


                         #2.GLS estimation
reg2 = sm.formula.gls('wage ~ experience + education',data)
reg2 = reg2.fit()
print(reg2.summary())


                        #3.Robust standard errors
reg3 =sm.formula.ols('wage ~ experience + education', data)
reg3 = reg3.fit(cov_type='HC1')
print(reg3.summary())

#====================================END================================================#










