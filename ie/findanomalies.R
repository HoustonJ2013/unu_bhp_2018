library(tidyverse)
library(dplyr)
library(foreach)
library(parallel)
library(lubridate)
library(zoo)
library(xts)
library(ggplot2)
library(AnomalyDetection)
require(data.table)
library(grid)
library(logging)
library(feather)
library(AnomalyDetection)
basicConfig()
addHandler(writeToFile, logger="anomalydetection", file="../data/anomalies.log")
petroleum.data = read_feather('../data/all_data.feather')

head(petroleum.data)

column.names = c("05-TT-29101-03_C1_Manifold_Temperature (DegF)",
                "05-TT-29101-02_C1_Manifold_Temperature (DegF)", 
                "05-PT-29101-02_C1_Manifold_Pressure (Psi)",
                "05-PT-29101-03_C1_Manifold_Pressure (Psi)",
                "05-TT-34101-04_H1_Manifold_Temperature (DegF)",
                "05-TT-34101-01_H1_Manifold_Temperature (DegF)",
                "05-PT-34101-04_H1_Manifold_Pressure (Psi)",
                "05-PT-34101-01_H1_Manifold_Pressure (Psi)",
                "05-TT-28201-01_B2_Manifold_Temperature (DegF)",
                "05-TT-28201-03_B2_Manifold_Temperature (DegF)",
                "05-PT-28201-01_B2_Manifold_Pressure (Psi)",
                "05-PT-28201-03_B2_Manifold_Pressure (Psi)",
                "05-PT-28201-01_B2_Manifold_Pressure (Psi)",
                "05-PT-28201-03_B2_Manifold_Pressure (Psi)",
                "05-PT-28201-01_B2_Manifold_Pressure (Psi)",
                "05-PT-28201-03_B2_Manifold_Pressure (Psi)")


head(petroleum.data)

datetime <- function(year, month, day, hour, minute)
{
  s = sprintf("%4d/%2d/%2d %2d:%2d",year, month, day, hour, minute )
  t = as.POSIXct(s, format="%Y/%m/%d %H:%M")
  return (t)
}

ExportPlot <- function(gplot, filename, width=8, height=4) {
  # Export plot in PDF and EPS.
  # Notice that A4: width=11.69, height=8.27
  dev.new()
  ggsave(filename, gplot, width = width, height = height)
  #print(gplot)
  dev.off()

}

start.times=c(datetime(2016, 10, 25, 10, 0), datetime(2016, 11, 15,10,0), datetime(2016, 11, 10,10,0), datetime(2016, 11, 26,10,0),
             datetime(2017, 1, 27,10,0), datetime(2017, 2, 18,10,0), datetime(2017, 3, 11,10,0))

end.times = c(datetime(2016, 10, 26, 10, 0), datetime(2016, 11, 16, 10,0),datetime(2016, 11, 11, 10,0),datetime(2016, 11, 27, 10,0), 
             datetime(2017, 1, 28, 10,0),datetime(2017, 2, 19, 10,0),datetime(2017, 3, 12, 10,0))

foreach (i = 1:NROW(start.times)) %do%
{
  start.time = start.times[i]
  end.time = end.times[i]
  for ( j in 1:NROW(column.names))
  {
    column.name = column.names[j]
    event.data = petroleum.data %>% filter(TimeStamp > start.time ) %>% filter(TimeStamp < end.time)
    x = as.data.frame(event.data[,c('TimeStamp', column.name)])
    names(x) = c('TimeStamp', 'y')
    res = AnomalyDetectionVec(x$y, max_anoms=0.05, direction='both', plot=TRUE, period = 2, alpha = 0.05)
    v=data.frame(x=event.data$TimeStamp[res$anoms$index], y=res$anoms$anoms)
    if(NROW(v)>0)
    {
      loginfo("Found %d anomalies in %s for time: %s - %s", NROW(v), column.name, start.time, end.time)
      p <-ggplot (x, aes(TimeStamp, y)) + 
        geom_line() + 
        geom_point(data=v, aes(x=x, y=y, colour='var2'))+
        theme_bw()+
        xlab('Timestamp') + 
        ylab(column.name)+
        theme(legend.position="none")
      file.name = sprintf('../data/%d_%d.pdf', i,j)
      ExportPlot(p, file.name)
      loginfo('Wrote file: %s', file.name)
    }else
    {
      loginfo("No anomalies in %s", column.name)
    }
  }
}

