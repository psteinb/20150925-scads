#!/bin/bash
export NO_CORES=12
export NO_NODES=16
export MEM=1900
export MEM_Global=$(($NO_CORES*$MEM))
export MEM_Driver=$(($MEM_Global / 2))
export MEM_Executor=$(($MEM_Global-$MEM_Driver))
export SPARK_DAEMON_MEMORY="${MEM_Driver}m"
export SPARK_MEM=$SPARK_DAEMON_MEMORY
srun -A zihforschung --tasks-per-node=1 --cpus-per-task=$NO_CORES --nodes=$NO_NODES --ntasks=$NO_NODES --mem-per-cpu $MEM --multi-prog conf/spark_multiprog.conf
