setwd("~/Documents/Git_Repos/Mind-Games-domino-solver") #set working directory

#Read in all relevant data
cost1 = read.csv("cost_list1.txt",header=FALSE)
best1 = read.csv("best_list1.txt",header=FALSE)
cost2 = read.csv("cost_list2.txt",header=FALSE)
best2 = read.csv("best_list2.txt",header=FALSE)

#Function for plotting the 3 lines
make_graph = function(cost,best) {
  plot(cost[,1], cost[,2], type="l", col="blue", lwd=1.5, xlab="Iterations", ylab="Cost") #plot cost
  
  smooth_cost = loess(cost[,2] ~ cost[,1]) #calculate smoothed cost
  lines(predict(smooth_cost), col="black", lwd=2.5) #plot smoothed cost
  
  lines(best[,1], best[,2], type="s", col="red", lwd=2.5) #plot best cost
}

#Plot each data set separately, along with its hand-positioned legend
make_graph(cost1,best1)
legend(25000, 65, c("cost","cost (smoothed)", "cost (best)"), lty=1, lwd=c(1.5,2.5,2.5), col=c("blue","black","red"), bty = "n")
make_graph(cost2,best2)
legend(38000, 65, c("cost","cost (smoothed)", "cost (best)"), lty=1, lwd=c(1.5,2.5,2.5), col=c("blue","black","red"), bty = "n")