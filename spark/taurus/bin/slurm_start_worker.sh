#!/bin/bash
function print_nodelist {
    scontrol show hostname $SLURM_NODELIST
}
MASTER_NODE="spark://$(print_nodelist | head -n 1):7077"
echo "Master -> $MASTER_NODE"
. /home/zihforschung/scads/spark/bin/spark-env.sh
$bin/spark-class org.apache.spark.deploy.worker.Worker $MASTER_NODE 

