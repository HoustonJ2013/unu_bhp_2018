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
basicConfig()

file1.name = "../data/Hackathon_DataSet_OctApr_Part1.txt"
file2.name = "../data/Hackathon_DataSet_OctApr_Part2.txt"
part1= as_tibble(fread(file1.name, sep="\t", stringsAsFactors = T, header=T))
part2= as_tibble(fread(file2.name, sep="\t", stringsAsFactors = T, header=T))


petroleum.data = part1 %>% inner_join (part2, by=c('Id' = 'Id', 'TimeStamp' = 'TimeStamp', 'hackathon4' = 'hackathon4', 'PIIntShapeID' = 'PIIntShapeID', 'PIIntTSTicks' = 'PIIntTSTicks')) 
petroleum.data$TimeStamp = as.POSIXct(as.character(petroleum.data$TimeStamp), format="%m/%d/%Y %I:%M:%S %p")
petroleum.data = petroleum.data %>% select(-one_of(c("hackathon4", "PIIntShapeID", "PIIntTSTicks" )))
head(petroleum.data)
write.csv(petroleum.data, '../data/hackathon_dataset_octapr_combined.csv')
start_time =as.POSIXct('15/11/2016 10:00:00', format="%d/%m/%Y %H:%M:%S")# datetime(2017, 3, 11,20,0)
end_time = as.POSIXct('16/11/2016 12:00:00', format="%d/%m/%Y %H:%M:%S") #datetime(2017, 3, 12, 13,0)

event.data = petroleum.data %>% filter(TimeStamp > start_time ) %>% filter(TimeStamp < end_time)
names(event.data)
p1 <- ggplot(event.data, aes(TimeStamp, `21-PT-10505.PV_Production_Separator (PSIG)` )) +
  geom_line() + theme_bw() +
  xlab('Time Stamp') + 
  labs("21-PT-10505.PV_Production_Separator (PSIG)" )

p2 <- ggplot(event.data, aes(TimeStamp, `05-PT-29101-02_C1_Manifold_Pressure (Psi)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('05-PT-29101-02_C1_Manifold_Pressure (Psi)')

p3 <- ggplot(event.data, aes(TimeStamp, `05-TT-29101-02_C1_Manifold_Temperature (DegF)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('05-TT-29101-02_C1_Manifold_Temperature (DegF)')

p4 <- ggplot(event.data, aes(TimeStamp, `21-LIC-10620.CV_2nd_Stg_Hydrocyclone_Wtr_Out (%)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('21-LIC-10620.CV_2nd_Stg_Hydrocyclone_Wtr_Out (%)')

p5 <- ggplot(event.data, aes(TimeStamp, `05-PT-28201-01_B2_Manifold_Pressure (Psi)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('05-PT-28201-01_B2_Manifold_Pressure (Psi)')

p6 <- ggplot(event.data, aes(TimeStamp, `05-TT-28201-01_B2_Manifold_Temperature (DegF)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('05-TT-28201-01_B2_Manifold_Temperature (DegF)')

p7 <- ggplot(event.data, aes(TimeStamp, `05-TT-33101-03_G1_Manifold_Temperature (DegF)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('05-TT-33101-03_G1_Manifold_Temperature (DegF)')

p8 <- ggplot(event.data, aes(TimeStamp, `05-PT-33101-03_G1_Manifold_Pressure (Psi)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('05-PT-33101-03_G1_Manifold_Pressure (Psi)')

p9 <- ggplot(event.data, aes(TimeStamp, `20-TT-20105.PV_Train_2_Subsea_Flowline_Launcher (Deg.F)`)) + 
  geom_line() + theme_bw() +
  xlab('Time Stamp') + ylab('20-TT-20105.PV_Train_2_Subsea_Flowline_Launcher (Deg.F)')


grid.newpage()
grid.draw(rbind(ggplotGrob(p1), 
                ggplotGrob(p2),
                ggplotGrob(p3),
                ggplotGrob(p4),
                ggplotGrob(p5),
                ggplotGrob(p6),
                ggplotGrob(p7),
                ggplotGrob(p8),size = "last"))


grid.newpage()
#drill center c

t1 <- ggplot(event.data, aes(TimeStamp)) +
  #geom_line(aes(y= `05-TT-29101-03_C1_Manifold_Temperature (DegF)`, colour = `05-TT-29101-03_C1_Manifold_Temperature (DegF)`)) + 
  geom_line(aes(y = `05-TT-29101-02_C1_Manifold_Temperature (DegF)`, colour = 'x1')) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill c Temp')


p1 <- ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `05-PT-29101-02_C1_Manifold_Pressure (Psi)`, colour = `05-PT-29101-02_C1_Manifold_Pressure (Psi)`)) + 
  #geom_line(aes(y = `05-PT-29101-03_C1_Manifold_Pressure (Psi)`, colour = `05-PT-29101-03_C1_Manifold_Pressure (Psi)`)) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill c Pressure')

#drill h
t2 <- ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `05-TT-34101-04_H1_Manifold_Temperature (DegF)`, colour = `05-TT-34101-04_H1_Manifold_Temperature (DegF)`)) + 
  geom_line(aes(y = `05-TT-34101-01_H1_Manifold_Temperature (DegF)`, colour = `05-TT-34101-01_H1_Manifold_Temperature (DegF)`)) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill H Temp')


p2 <- ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `05-PT-34101-04_H1_Manifold_Pressure (Psi)`, colour = `05-PT-34101-04_H1_Manifold_Pressure (Psi)`)) + 
  geom_line(aes(y =`05-PT-34101-01_H1_Manifold_Pressure (Psi)`, colour =`05-PT-34101-01_H1_Manifold_Pressure (Psi)`)) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill H Pressure')


#drill b
t3 <- ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `05-TT-28201-01_B2_Manifold_Temperature (DegF)`, colour = `05-TT-34101-04_H1_Manifold_Temperature (DegF)`)) + 
  geom_line(aes(y =`05-TT-28201-03_B2_Manifold_Temperature (DegF)`, colour = `05-TT-34101-01_H1_Manifold_Temperature (DegF)`)) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill B Temp')


p3 <- ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `05-PT-28201-01_B2_Manifold_Pressure (Psi)`,  colour = `05-PT-34101-04_H1_Manifold_Pressure (Psi)`)) + 
  geom_line(aes(y =`05-PT-28201-03_B2_Manifold_Pressure (Psi)`, colour =`05-PT-34101-01_H1_Manifold_Pressure (Psi)`)) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill B Pressure')

#drill center G
t4 <- ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `05-TT-33101-03_G1_Manifold_Temperature (DegF)`, colour = `05-TT-34101-04_H1_Manifold_Temperature (DegF)`)) + 
  geom_line(aes(y =`05-TT-33101-02_G1_Manifold_Temperature (DegF)`, colour = `05-TT-34101-01_H1_Manifold_Temperature (DegF)`)) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill G Temp')


p4 <- ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `05-PT-33101-03_G1_Manifold_Pressure (Psi)`,  colour = `05-PT-34101-04_H1_Manifold_Pressure (Psi)`)) + 
  geom_line(aes(y =`05-PT-33101-02_G1_Manifold_Pressure (Psi)`, colour =`05-PT-34101-01_H1_Manifold_Pressure (Psi)`)) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Drill G Pressure')

#production separator
ps =  ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `21-LIC-10516.SP_Prod_Sep_Oil_Out_To_2nd_Stg_Sep (%)`,  colour = "v1")) + 
  geom_line(aes(y =`21-LT-10516.PV_Prod_Sep_Oil_Interface_Level (%)`, colour ="V2")) +
  geom_line(aes(y =`21-LY-10516.OUT_Prod_Sep_Oil_Out_To_2nd_Stg_Sep (%)`, colour ="V3")) +
  geom_line(aes(y =`21-LIC-40516.SP_Test_Allocation_Sep_Interface (%)`, colour ="V4")) +
  geom_line(aes(y =`21-LT-40516.PV_Test_Allocation_Sep_Interface (%)`, colour ="V5")) +
  geom_line(aes(y =`21-LY-40516.OUT (%)`, colour ="V6")) +
  
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Production separator (%)')

psg = ggplot(event.data, aes(TimeStamp)) +
  geom_line(aes(y= `21-PT-10505.PV_Production_Separator (PSIG)`,  colour = "v1")) + 
  geom_line(aes(y= `21-PT-40505.PV_Test_Allocation_Separator (PSIG)`,  colour = "v2")) + 
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Production separator PSIG')


bpd = ggplot(event.data, aes(TimeStamp)) +

  geom_line(aes(y =`21-FQI-10518-01.NetRate.PV (BPD)`, colour ="V2")) +
  theme_bw()+
  theme(legend.position="none")+
  xlab('Time Stamp') + ylab('Production separator bpd')


grid.draw(rbind(ggplotGrob(p1), 
                ggplotGrob(p2),
                ggplotGrob(p3),
                ggplotGrob(p4),
                ggplotGrob(t1),
                ggplotGrob(t2),
                ggplotGrob(t3),
                ggplotGrob(t4),
                ggplotGrob(ps),
                ggplotGrob(psg),
                ggplotGrob(bpd),
                size = "last"))


library(AnomalyDetection)
x = as.data.frame(event.data %>% select(TimeStamp,y= `05-PT-29101-02_C1_Manifold_Pressure (Psi)`))
res = AnomalyDetectionVec(x$y, max_anoms=0.05, direction='both', plot=TRUE, period = 2)
res$plot


v=data.frame(x=event.data$TimeStamp[res$anoms$index], y=res$anoms$anoms)

ggplot (x, aes(TimeStamp, y)) + 
  geom_line() + 
  geom_point(data=v, aes(x=x, y=y, colour='var2'))+
  theme_bw()+
  xlab('Timestamp') + 
  ylab('Pressue at 29101-02_C1')+
  theme(legend.position="none")


x = as.data.frame((event.data %>% select(TimeStamp, y=`21-LT-10516.PV_Prod_Sep_Oil_Interface_Level (%)`)))
res = AnomalyDetectionVec(x$y, max_anoms=0.05, direction='both', plot=TRUE, period = 2, alpha = 0.02)


v=data.frame(x=event.data$TimeStamp[res$anoms$index], y=res$anoms$anoms)

ggplot (x, aes(TimeStamp, y)) + 
  geom_line() + 
  geom_point(data=v, aes(x=x, y=y, colour='var2'))+
  theme_bw()+
  xlab('Timestamp') + 
  ylab('Production Separator 10516.SP_Prod_Sep_Oil_Out')+
  theme(legend.position="none")


x = as.data.frame((event.data %>% select(TimeStamp, y=`05-TT-29101-02_C1_Manifold_Temperature (DegF)`)))
res = AnomalyDetectionVec(x$y, max_anoms=0.05, direction='both', plot=TRUE, period = 2, alpha = 0.02)


v=data.frame(x=event.data$TimeStamp[res$anoms$index], y=res$anoms$anoms)

ggplot (x, aes(TimeStamp, y)) + 
  geom_line() + 
  geom_point(data=v, aes(x=x, y=y, colour='var2'))+
  theme_bw()+
  xlab('Timestamp') + 
  ylab('Temperature at 29101-02_C1')+
  theme(legend.position="none")


#acf
total = as.data.frame(petroleum.data %>% select(x= `05-PT-29101-02_C1_Manifold_Pressure (Psi)`, 
                                            y = `21-LT-10516.PV_Prod_Sep_Oil_Interface_Level (%)`))

corr_ = acf(total, 2000)

y = corr_$acf[,1,2]
t = (0:(NROW(y)-1))*(0.5/60)
ar = data.frame(lag=t, corr=y)
ggplot(ar, aes(lag, corr)) +
  geom_line(colour = 'red') + 
  theme_bw() +
  xlab('Lag (Hours)') + ylab('Correlation Correlation between Pressure 29101 and Prod Sep 10516')
