

#from __future__ import print_function
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

import sys
import os
import hashlib
import glob

from operator import add
from pyspark import SparkContext


if __name__ == "__main__":
    """
        Usage: dist_md5sum [directory-to-use]
    """

    this_file_name = os.path.basename(__file__)
    path_to_parse = None
    if len(sys.argv) < 2:
        path_to_parse = os.path.abspath(os.curdir)
    else:
        if os.path.exists(sys.argv[1]):
            path_to_parse = os.path.abspath(sys.argv[1])
        else:
            print "[%s] unable to parse given path %s! Does it exists?" % (this_file_name,sys.argv[1])
            sys.exit(1)

    filelist = glob.glob(path_to_parse+"/*")
    print "[%s] distributing %i files from %s" % (this_file_name,len(filelist),path_to_parse)
    
    sc = SparkContext(appName="PythonMD5SUM")
    #sc.setLogLevel("ALL")
    
    def f(_filename):
        return "%s %s\n" % (hashlib.md5(open(_filename,'rb').read()).hexdigest(), _filename)

    # def join(_left, _right):
    #     value = _left
    #     value += "\n" + _right
        
    md5list = sc.parallelize(filelist).map(f).reduce(add)
    
    sc.stop()
    
    res_file = open(path_to_parse+"/md5sum.log","w")
    res_file.writelines(md5list)
    res_file.close()
