        
#=======================CLEARING MEMORY=========================#
rm(list=ls()) 
gc() 
cat("\f") 
ls() 

#========================INSTALL PACKAGES=======================#

install.packages("lmtest")     #install ONLY if you do not have
install.packages("ggplot2")    #install ONLY if you do not have
install.packages("AER")        #install ONLY if you do not have
install.packages("nlme")       #install ONLY if you do not have
install.packages("sandwich")   #install ONLY if you do not have
#==========================LOAD LIBRARIES=======================#

library(lmtest)
library(ggplot2)
library(AER) 
library(nlme)
library(sandwich)
#==========================LOAD DATA============================#

#1.Data
data(CPS1985)
#2.attach
attach(CPS1985)
#===========================DESCRIPTIVES========================#               

View(CPS1985)
head(CPS1985)
summary(CPS1985)
head(CPS1985)
tail(CPS1985)

#========================REGRESSION=============================#

#1.level model
reg <-lm(wage~education+experience)
summary(reg)

#Statistical test:Breusch-Pagan test
bptest(reg)

#======================RESOLVING HETEROSKEDASTICITY=============#

lnwage <- log(wage)
lneduc <- log(education)
lnexper <- log(experience)

                   #1.Changing functional forms

#i.logging dependent variable

log_depvar <-lm(lnwage~education+experience)
summary(log_depvar)
bptest(log_depvar)                       #No heteroskedasticity

#ii.logging dependent and independent variable
log_allvar <-lm(lnwage~lneduc + experience)
summary(log_allvar)
bptest(log_allvar)                        #No heteroskedasticity

         
           #2.Generalized least squares estimation
gl <- gls(wage~education+experience,CPS1985)
summary(gl)

                  #3.White standard errors 
#i.original model results
coeftest(reg, vcov = vcovHC(reg, type = "HC0"))

#=====================ENDING R SESSION==========================#

dev.off()
rm(list=ls())
gc() 
cat("\f")
            
