
#=====================INSTALL LIBRARIES=========================#

#Do this step if the packages ARE NOT installed
install.packages("lmtest")
install.packages("dyplyr")
install.packages("ggplot2")
install.packages("olsrr")

#======================LOAD LIBRARIES===========================#
library(lmtest)
library(dplyr)
library(ggplot2)
library(olsrr)
#===========================DATA================================#

data(trees)
data(mtcars)
print(trees)
print(mtcars)

#==============CREATING A DESCRIPTIVES FUNCTION=================#

#regression and heteroskedasticity ftn

descripDf <- function(df) { # outline descriptive stats i want 
                            strDf <- str(df)
                            headDf<- head(df)
                            tailDf<-tail(df)
                           summaryDf <-summary(df)
                           
                           #output list from function
                        summary_list <-list(strDf,headDf,
                                            tailDf,summaryDf)
                          return(summary_list)
  
}

#================DESCRIPTIVES:BASED ON FUNCTION ================#

#1.calling descriptive function for trees dataset
descripDf(trees)

#2.calling on descriptive function for cars dataset
descripDf(mtcars)

#=======================REGRESION===============================#

reg_ftn <- function(y,x) {
                             reg <- lm(y~x)
                             reg_summary <- summary(reg)
                             
                             #heteroskedasticity tests
                             bp_test <- bptest(reg)
                             score_test <- ols_test_score(reg)
                             f_test <- ols_test_f(reg)
                             
                             #output list from function
                             reg_list <- list (reg,reg_summary,
                                               bp_test,
                                               score_test,f_test)
                            
                             return(reg_list)
}

#=============REGRESSION:calling function=========================#

#==========Regression 1: mtcars data

#defining model for mtcars data
xMtcars <- cbind(cyl,disp)
yMtcars <- cbind(mpg)

#calling the reg function for mtcars model
#and heteroskedasticity
reg_ftn(yMtcars,xMtcars)

#==========Regression 2: trees data
#defining model for trees data

xTrees <- cbind(Height,Girth)
yTrees <- cbind(Volume)
reg_ftn(yTrees,xTrees)

#===================END=========================================#
