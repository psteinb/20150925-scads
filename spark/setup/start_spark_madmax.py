#! /usr/bin/python
import os, socket, sys, re

spark_dir = os.getenv('SPARK_HOME')
if not spark_dir:
    spark_dir = os.getenv('HOME')+"/spark"
spark_sbin = spark_dir + '/sbin'

# figure out which hosts we have
pat = re.compile('[e]\d+')
hosts = pat.findall(os.environ.get('LSB_MCPU_HOSTS'))

print os.getenv('LSB_MCPU_HOSTS')

# main host
my_host = socket.gethostname()
max_cores_per_node = 12

# set up slave file
slave_file = '%s/slaves_%s'%(os.getenv('HOME'),os.getenv('LSB_JOBID'))

# set up the slaves file
with open(slave_file,'w') as slaves:
    for host in hosts :
        slaves.write("%s\n"%host)

if  __name__ == "__main__":
    import getopt

    # set defaults
    mem = None #os.environ.get('SPARK_MEMORY','2g')
    cores = None

    try  :
        opts, args  = getopt.getopt(sys.argv[1:], "m:c:")
    except getopt.GetoptError :
        usage()
        sys.exit(2)

    for opt, arg in opts :
        if opt == '-m' :
            mem = arg

        if opt == '-c' :     # set to 12 if sufficient memory
            cores = arg
	else : 
	    cores = 12

    if mem is not None: os.environ['SPARK_EXECUTOR_MEMORY'] = mem

    os.environ['SPARK_SLAVES'] = slave_file

    master_command = '%s/start-master.sh' % spark_sbin

    cores_per_slave = cores/max_cores_per_node
    
    slaves_command = 'mpirun -np %i --map-by ppr:1:node %s/start-slave.sh spark://%s:7077 -c %i' % (cores,
                                                                                                    spark_sbin,
                                                                                                    my_host,
                                                                                                    cores_per_slave)
    if mem:
        slaves_command += " -m " % (mem.upper())

    slaves_command += " &"
        
    print slaves_command

    # start the host and slaves
    print 'master command ', master_command
    print 'slaves command ', slaves_command
    os.system(master_command)
    os.system(slaves_command)
