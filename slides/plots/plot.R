#!/usr/bin/env Rscript

argv = commandArgs(TRUE)

if(length(argv) < 1){
    stop("Usage: plot.R <data_file> <data_file>")
}

sparkfile <- argv[1]

if(length(argv) > 1){
standalonefile <- argv[2]
} 

spark_data <- read.table(sparkfile, header = T,stringsAsFactors=TRUE)
standalone_data <- read.table(standalonefile, header = T,stringsAsFactors=TRUE)

library(ggplot2)
library(dplyr)

filtered_data <- filter(bench_data, id != "_lrt")

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
                             legend.margin=unit(1, "pt"),
#                             legend.justification=c(0,0),
                             legend.key = element_rect(colour = 'white', fill = 'white', size = 0., linetype='dashed')) #+ theme(legend.title=element_blank()) 


mse_plot <- ggplot(filtered_data, aes(x=bw_mb_p_sec,
                                      y=compression_ratio,
                                      size=mse,
                                      shape=literal_id,
                                      color=brieffname)) 
mse_plot <- mse_plot + geom_point() + ylim(75,175)
mse_plot <- mse_plot + ylab("raw_size/compressed_size") + xlab("ingest bandwidth [MB/s]") + guides(col=guide_legend(ncol=3))
mse_plot <- mse_plot + guides(color=FALSE) + scale_shape_discrete(name="Type") 
mse_plot <- mse_plot + my_theme #+  theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank())


ggsave("spark_scale_",mse_plot)
ggsave("spark_scale_",mse_plot)
ggsave("spark_scale_",mse_plot)

