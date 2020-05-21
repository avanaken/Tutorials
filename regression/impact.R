library(CausalImpact)


data <- data.frame(data)
pre.period <- c(1, 331)
post.period <- c(332,400)

impact <- CausalImpact(data, pre.period, post.period,model.args = list(niter = 5000))
plot(impact)
