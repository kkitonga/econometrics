
#==========================SCRIPT DETAILS========================----

#Script author:kkitonga
#date:21/06/2022
#details:Impact assessment : endogenous switching regression

#=====================INSTALL PACKAGES==========================----

#Package Installation :do this ONLY if the package is not installed
install.packages("endoSwitch")
install.packages("DataExplorer")
install.packages("ggplot2")
install.packages("dplyr")
install.packages("broom")

#======================LOAD PACKAGE==============================----

library(endoSwitch)
library(DataExplorer)
library(ggplot2)
library(dplyr)
library(broom)

#======================LOAD DATA================================----

data(ImpactData)
print(ImpactData)
attach(ImpactData)

#======================DATA OVERVIEW==============================----

#Base R :data overview
View(ImpactData)
head(ImpactData)
str(ImpactData)
summary(ImpactData)

#Dplyr:Summarize select variables by group
summary<-ImpactData%>%
         group_by(CA)%>%
        summarise(across(1:4,list(mean=mean)))

#Data explorer
create_report(ImpactData)

#============DESCRIPTIVES :ADOPTERS  VS NON-ADOPTERS================#

#1.Descriptive----
#i.Box-plot:adopters and non-adopters

boxplot(Output~CA)

#ii.#insight into variances in output between two groups
var(Output[CA==1])
var(Output[CA==0])
 
#iii.Help t-test(Two-sample test) :Adopters versus non-adopters
help(t.test)

#iv.hypothesis 
#Ho: mean ["variable name"] of adopters= non-adopters
#H1: mean ["variable name"] of adopters!= non-adopters

#v.full t.test function
t.test(Output~CA,
       alternative = "two.sided",
       mu = 0, paired = FALSE, var.equal = FALSE,
       conf.level = 0.95)

#vi.short syntax : select variables by CA 

tidy(t.test(Age~CA))
tidy(t.test(Land_holding~CA))
tidy(t.test( Farm_size,CA))
tidy(t.test(Access_to_credit~CA))
tidy(t.test(Distance_to_market~CA))
tidy(t.test(Distance_to_capital~CA))

#=======================VISUALIZATION===============================#

#2.Density plot of logged output :non-adopters and adopters

#i.creating a dataframe"dat" with an additional variable "status"
   #derived from the variable "CA".

dat<-ImpactData %>%
       mutate(status=case_when(CA==1 ~"adopters",
                          CA==0 ~"non-adopters",
                          TRUE~ ""
                          )
              )

#ii.Plot1EndoSwitch:adopters versus non-adopters(with fill)

dat %>%
       ggplot(aes(log(Output),color= status,fill=status))+
       geom_density()+
       labs(x="Maize output(logged)",title="distribution of maize output :non-adopters vs adopters")

#iii.Plot2EndoSwitch: adopters versus non-adopters (no fill)

dat %>%
       ggplot(aes(log(Output),color= status))+
       geom_density()+
       labs(x="Maize output(logged)",title="distribution of maize output :non-adopters vs adopters")


#iv.Plot3EndoSwitch: adopters versus non-adopters

dat %>%
       ggplot(aes(log(Output)))+
       geom_density()+
       facet_wrap(~status)+
       labs(x="Maize output(logged)",title="distribution of maize output :non-adopters vs adopters")

#==================MODEL========================================----

#3.Endogenous switching regression model----

OutcomeDep <- 'Output'
SelectDep <- 'CA'
OutcomeCov <- c('Age')
SelectCov <- c('Age', 'Perception')
endoReg <- endoSwitch(ImpactData, OutcomeDep, 
                      SelectDep, OutcomeCov, SelectCov)
summary(endoReg)

#=================TWO STAGE ESTIMATION===========================----

#4.ESR :Two stage regression----

#i.Running regression
Results <- endoSwitch2Stage(ImpactData, OutcomeDep, 
                            SelectDep, OutcomeCov, SelectCov)

#ii.First stage regression results
summary(Results$FirstStageReg)

#iii. Second stage regression results: non-adopter
summary(Results$SecondStageReg.0)

#iv. Second stage regression results:adopter
summary(Results$SecondStageReg.1)


#=======================END===========================================
