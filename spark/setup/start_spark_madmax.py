#! /usr/bin/python
import os
import sys
import re
import subprocess

spark_dir = os.getenv('SPARK_HOME')
if not spark_dir:
    spark_dir = os.getenv('HOME')+"/spark"
spark_sbin = spark_dir + '/sbin'

# figure out which hosts we have
pat = re.compile('[n]\d+')
lsb_mcpu_hosts = os.getenv('LSB_MCPU_HOSTS')
hosts = pat.findall(lsb_mcpu_hosts)

print ">> LSB_MCPU_HOSTS",lsb_mcpu_hosts
print ">> found hosts: ", hosts

master_ip = os.getenv("HOSTNAME")

# set up slave file
slave_file = '%s/slaves_%s' % (os.getenv('HOME'),os.getenv('LSB_JOBID'))


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
        if opt == '-s' :
            if os.path.exists(arg) and os.path.is_directory(arg):
                slave_file = '%s/slaves_%s' % (arg,os.getenv('LSB_JOBID'))
                os.environ['SPARK_LOCAL_DIRS']=arg

    # set up the slaves file
    with open(slave_file,'w') as slaves:
        for host in hosts :
            slaves.write("%s\n"%host)

            
    if mem is not None:
        os.environ['SPARK_EXECUTOR_MEMORY'] = mem.upper()

    os.environ['SPARK_SLAVES'] = slave_file

    master_command = '%s/start-master.sh' % spark_sbin

    # start the master
    print 'master command ', master_command
    mc = subprocess.check_output(master_command.split())
    print mc
    print "master set to ",master_ip
    
    
    #http://stackoverflow.com/questions/28216897/syntax-of-the-map-by-option-in-openmpi-mpirun-v1-8
    # slaves_command = 'mpirun -np %i %s/start-slave.sh spark://%s:7077 -c 1' % (int(cores),
    #                                                                            spark_sbin,
    #                                                                            master_ip)

    #start the slaves/workers
    n_slaves_used = len(hosts)    
    hnc_pat = re.compile('[n]\d+ \d+')
    hosts_and_cores = hnc_pat.findall(lsb_mcpu_hosts)
    cnt = 0
    for t in hosts_and_cores:
        node,recv_cores = t.split()
        cmd = "ssh %s %s/start-slave.sh  -c %i" % (node,spark_sbin,int(recv_cores))
        if mem:
            cmd += " -m %s" % (mem.upper())
        cmd += " spark://%s:7077 &" % master_ip
        output = subprocess.check_output(cmd.split())
        print ">> slave %i/%i\t%s" % (cnt,n_slaves_used,cmd)
        print output
        cnt+=1



