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
standalone_data
spark_data <- read.table(sparkfile, header = T,stringsAsFactors=TRUE)
spark_data$speedup <- mean(standalone_data$duration_s) / spark_data$duration_s 
spark_data
library(ggplot2)
## library(dplyr)

## filtered_data <- filter(bench_data, id != "_lrt")

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

ggsave("spark_standalone.png",standalone_plot)
ggsave("spark_standalone.svg",standalone_plot)


spark_plot <- ggplot(spark_data, aes(x=factor(n_cores),
                                      y=speedup)) 
spark_plot <- spark_plot + geom_point(size=5) #+ geom_point(data=standalone_data,aes(y=duration_s),color=2)
spark_plot <- spark_plot + ylab("speed up") + xlab("Cores") 
spark_plot <- spark_plot + my_theme #+  theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank())
spark_plot <- spark_plot + geom_hline(data=standalone_data,aes(yintercept=1),   # Ignore NA values for mean
               color="red", linetype="dashed", size=1)

ggsave("spark_scaling.png",spark_plot)
ggsave("spark_scaling.svg",spark_plot)

