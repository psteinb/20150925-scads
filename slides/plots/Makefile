all:
	# ./plot.R xpi_gpu.data pythonpi_local.data
	# mv scaling_to_standalone.png scalapi_spark_scaling.png
	# mv scaling_to_standalone.svg scalapi_spark_scaling.svg
	# convert -resize 1000x scalapi_spark_scaling.png scalapi_spark_scaling_1000x.png

	# ./plot.R ../../spark/data/spark_bootstrap.data ../../spark/data/standalone.data
	# mv scaling_to_standalone.png bootstrap_spark_scaling.png
	# mv scaling_to_standalone.svg bootstrap_spark_scaling.svg
	# convert -resize 1000x bootstrap_spark_scaling.png bootstrap_spark_scaling_1000x.png 

	./plot.R ../../spark/data/xpi.data ../../spark/data/pythonpi_local.data
	mv scaling_to_standalone.png scalapi_spark_scaling_to_standalone.png
	convert -resize 900x scalapi_spark_scaling_to_standalone.png scalapi_spark_scaling_to_standalone_900x.png
	mv scaling_to_self.png scalapi_spark_scaling_to_self.png
	convert -resize 900x scalapi_spark_scaling_to_self.png scalapi_spark_scaling_to_self_900x.png
