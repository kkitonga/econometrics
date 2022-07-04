#@author: Kavengi
#Date:01/07/2022
#topic:linear regression

#==========================LOADING LIBRARIES==========================#
library(ggplot2)
library(dplyr)

#========================LOADING DATA=================================#

data(mtcars)
print(mtcars)
?mtcars
View(mtcars)
#============================DESCRIPTIVES============================#

head(mtcars)
tail(mtcars)

#============================REGRESSION==============================#

reg <- lm(mpg~wt,mtcars)
summary(reg)
#============================PLOTS===================================#

#MtCarsScatter.png

ggplot(data=mtcars,aes(wt,mpg))+
geom_point()+
labs(title="Scatterplot of Miles/per gallon vs Weight")

mtcars%>%
         ggplot(aes(wt,mpg))+
         geom_point(color="red")+
         labs(x="weight",y="miles per gallon",
              title="Scatterplot of Miles/per gallon vs Weight")

#=========================END========================================#

