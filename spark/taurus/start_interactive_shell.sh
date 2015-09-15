#!/bin/bash
. /home/zihforschung/scads/spark/bin/spark-env.sh
$bin/spark-shell --master `cat $HOME/spark_master.tmp`

