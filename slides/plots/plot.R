#!/usr/bin/env Rscript

argv = commandArgs(TRUE)

if(length(argv) < 1){
    stop("Usage: plot.R <data_file> <data_file>")
}

sparkfile <- argv[1]

if(length(argv) > 1){
standalonefile <- argv[2]
} 

standalone_data <- read.table(standalonefile, header = T,stringsAsFactors=TRUE)
head(standalone_data)

scaling_data <- read.table(sparkfile, header = T,stringsAsFactors=TRUE)

scaling_data$speedup2standalone <- mean(standalone_data$duration_s) / scaling_data$duration_s 



library(ggplot2)
library(dplyr)

mincores <- min(scaling_data$n_cores)
mincores_data <- filter(scaling_data, n_cores == mincores)
divide_by <- mean(mincores_data$duration_s)
divide_by
scaling_data$speedup2self <- divide_by / scaling_data$duration_s 
head(scaling_data)

my_theme <-  theme_bw() + theme(axis.title.x = element_text(size=20),
                                axis.title.y = element_text(size=20),
                                axis.text.x = element_text(size=16),
                                axis.text.y = element_text(size=16),
                                axis.text.x  = element_text()
                                ) 
my_theme <- my_theme + theme(legend.title = element_text(size=22, face="bold"),
                             legend.text = element_text( size = 20),
                             ## legend.text.align=0,
                             ## legend.title.align=0,
                             legend.position="top",
#                             legend.position=c(0, 1.),
                             legend.box.just="left",
                             
#                             legend.justification=c(0,0),
                             legend.key = element_rect(colour = 'white', fill = 'white', size = 0., linetype='dashed')) #+ theme(legend.title=element_blank()) 


standalone_plot <- ggplot(standalone_data, aes(x=n_cores,
                                      y=duration_s)) 
standalone_plot <- standalone_plot + geom_point() 
standalone_plot <- standalone_plot + ylab("runtime / s") + xlab("N_cores") 
standalone_plot <- standalone_plot + my_theme #+  theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank())

ggsave("scaling_standalone.png",standalone_plot)
ggsave("scaling_standalone.svg",standalone_plot)


scaling_plot <- ggplot(scaling_data, aes(x=factor(n_cores),
                                      y=speedup2standalone)) 
scaling_plot <- scaling_plot + geom_boxplot() + geom_jitter() 
scaling_plot <- scaling_plot + ylab("speed up") + xlab("Cores") + ylim(0,5) 
scaling_plot <- scaling_plot + my_theme #+  theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank())
scaling_plot <- scaling_plot + geom_hline(data=standalone_data,aes(yintercept=1),   # Ignore NA values for mean
               color="red", linetype="dashed", size=1)
scaling_plot <- scaling_plot + geom_abline(intercept = 0,slope=1,colour = "green", size = 2) #+ geom_point(size=5)
ggsave("scaling_to_standalone.png",scaling_plot)
ggsave("scaling_to_standalone.svg",scaling_plot)

scaling2self_plot <- ggplot(scaling_data, aes(x=factor(n_cores),
                                      y=speedup2self)) 
scaling2self_plot <- scaling2self_plot + geom_boxplot() + geom_jitter() + ylim(0,5) 
scaling2self_plot <- scaling2self_plot + ylab("speed up") + xlab("Cores") 
scaling2self_plot <- scaling2self_plot + my_theme #+  theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank())
scaling2self_plot <- scaling2self_plot + geom_hline(data=standalone_data,aes(yintercept=1),color="red", linetype="dashed", size=1)
scaling2self_plot <- scaling2self_plot + geom_abline(intercept = 0,slope=1,colour = "green", size = 2) #+ geom_point(size=5)

ggsave("scaling_to_self.png",scaling2self_plot)
ggsave("scaling_to_self.svg",scaling2self_plot)


