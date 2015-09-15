#!/usr/bin/env bash

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Starts the master on the machine this script is executed on.
. /home/zihforschung/scads/spark/bin/spark-env.sh
#spark_directory=/projects/p044/zihforschung/scads/spark/spark-1.3.1
#bin=$spark_directory/bin
#sbin=$spark_directory/sbin

. "$sbin/spark-config.sh"

. "$SPARK_PREFIX/bin/load-spark-env.sh"

if [ "$SPARK_MASTER_PORT" = "" ]; then
  SPARK_MASTER_PORT=7077
fi

if [ "$SPARK_MASTER_IP" = "" ]; then
  SPARK_MASTER_IP=`hostname`
fi

if [ "$SPARK_MASTER_WEBUI_PORT" = "" ]; then
  SPARK_MASTER_WEBUI_PORT=8080
fi
echo "spark://$SPARK_MASTER_IP:$SPARK_MASTER_PORT" > $HOME/spark_master.tmp

"$bin"/spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_IP --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT
