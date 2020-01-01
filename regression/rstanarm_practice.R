library('rstanarm')
library(tidybayes)

#for this example we are using credit card fraud

credit <- read.csv('/Users/andrew.van.aken/Downloads/creditcard.csv')

#Let's first define some items

#RHat - a measure of within chain variance compared to across chain variance.
#Values of less than 1 mean they converge

#Need to set prior for model
t_prior <- student_t(df = 7, location = 0, scale = 1)

#stan_glm is the general way to use the package and the family changes between
#logistic/regular regression

#Chains, iterations and warmup are set to the default values in R

post1 <- stan_glm(Amount ~ V1+V2+V3, data = credit,
                  chains=4, iter=2000,warmup=1000,
                  family = gaussian(), 
                  prior = t_prior, prior_intercept = t_prior,
                  seed = SEED)
summary(post1)
pplot<-plot(post1, "areas", prob = 0.95, prob_outer = 1)
pplot+ geom_vline(xintercept = 0)

##credible interval vs confidence interval
#Confidence interval -  probability that a range contains a true value
#Credible interval - probability that the true value falls in this range

#Here we are identifying the posterior interval using rstanarm, where prob is
#the interval to use

round(coef(post1), 2)
round(posterior_interval(post1, prob = 0.80), 2)

posterior <- spread_draws(post1,V1)
mean(between(poster))