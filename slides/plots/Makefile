all:
	./plot.R xpi_gpu.data pythonpi_local.data
	mv spark_scaling.png scalapi_spark_scaling.png
	mv spark_scaling.svg scalapi_spark_scaling.svg
	convert -resize 1000x scalapi_spark_scaling.png scalapi_spark_scaling_1000x.png

	./plot.R spark_bootstrap.data standalone.data
	mv spark_scaling.png bootstrap_spark_scaling.png
	mv spark_scaling.svg bootstrap_spark_scaling.svg
	convert -resize 1000x bootstrap_spark_scaling.png bootstrap_spark_scaling_1000x.png 
