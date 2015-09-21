

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

from bootstrap_utils import *
from skimage import io



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

    filelist = glob.glob(path_to_parse+"/*jpg")
    filelist.extend(glob.glob(path_to_parse+'/*tiff') )
    filelist.extend(glob.glob(path_to_parse+'/*tif') )
    filelist.extend(glob.glob(path_to_parse+'/*jpg') )
    filelist = [ item for item in filelist if item.count("_c")<1 and item.count("_r")<1 ]

    split_filelist = [ os.path.splitext(path) for path in filelist ]
    list_to_rotate = [item[0]+"_c"+item[1] for item in split_filelist]

    print "[%s] distributing %i files from %s" % (this_file_name,len(filelist),path_to_parse)
    
    
    #sc.setLogLevel("ALL")
    
    def color_image(_fname,_name_insert='_c'):

        image = io.imread(_fname)
        image = random_enhance_color(value)
        namebase,nameext = os.path.splitext(_fname)
        name2save = namebase+_name_insert+nameext
        io.imsave(name2save,image)
        
        return "%s %s\n%s %s\n" % (hashlib.md5(open(_fname,'rb').read()).hexdigest(),
                                   _fname,
                                   hashlib.md5(open(name2save,'rb').read()).hexdigest(),
                                   name2save)

    def rotate_image(_fname,_name_insert='_r'):
        image = io.imread(_fname)

        rvalue = ""
        
        for i in range(3):
            result = random_rotate(image)
            namebase,nameext = os.path.splitext(_fname)
            name2save = namebase+_name_insert+str(i)+nameext
            io.imsave(name2save,result)
            rvalues += "%s %s\n" % (hashlib.md5(open(name2save,'rb').read()).hexdigest(),
                                    name2save)

        return rvalue
        

    sc = SparkContext(appName="PythonBootstrap")
    
    colorlist = sc.parallelize(filelist).map(color_image).reduce(add)

    rotatedlist = sc.parallelize(list_to_rotate).map(rotate_image).reduce(add)
    
    sc.stop()
    
    rep1_file = open(path_to_parse+"/color_report","w")
    rep1_file.writelines(colorlist)
    rep1_file.close()

    rep2_file = open(path_to_parse+"/rotate_report","w")
    rep2_file.writelines(rotatedlist)
    rep2_file.close()
