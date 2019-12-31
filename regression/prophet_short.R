
library(prophet)

#read in the filename here

colnames(df) <- c('ds','y')
#df <- df[df$y<10000,]

m <- prophet(df)
future <- make_future_dataframe(m, periods = 365)
tail(future)
forecast <- predict(m, future)
tail(forecast[c('ds', 'yhat', 'yhat_lower', 'yhat_upper')])
plot(m, forecast)
prophet_plot_components(m, forecast)



