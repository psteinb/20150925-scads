---
title: Parallel Processing Pipelines 
subtitle: A User's Exploration with Apache Spark and Snakemake
author: Peter Steinbach
date: September 25, 2015
---

# Outline

## 

<div style="font-size: 2em;text-align: center;">
1. Background

2. Bazaar

3. Cathedral
</div>

# 

## MPI CBG

[columns,class="row vertical-align"]

[column,class="col-xs-8"]

![Some comments including license](img/1280px-MPI-CBG_building_outside_4pl.jpg)

[/column]

[column,class="col-xs-4"]

* 500 staff
* 50 % non-german
* founded 2001
* cell biology
* genomics
* systems biology

[/column]

[/columns]

## microscopes

[columns,class="row vertical-align"]

[column,class="col-xs-6"]

**Zeiss Lightsheet Z.1**

![[MPI-CBG LMF](http://www.biodip.de/wiki/LZ1_-_Zeiss_Lightsheet_Z.1) (no license)](img/LZ1_-_Zeiss_Lightsheet_Z.1_600p.jpg)

[/column]

[column,class="col-xs-6"]

**T-SPIM Farm**

![[openspim.org](http://openspim.org/Gallery) (no license)](img/2I_1D_OpenSPIM_farm_02_x450_cropped.jpg)

[/column]

[/columns]

[columns,class="row vertical-align"]

[column,class="col-xs-6"]

* commercial system (2 inhouse)
* 120 MB/s data production
* at best: operated 24/7

[/column]

[column,class="col-xs-6"]

* custom systems (>6 inhouse) 
* 850 MB/s data production
* at best: operated 24/7

[/column]

[/columns]


## Parallel Processing Essential 

![[flickr.com](https://www.flickr.com/photos/83633410@N07/7658225516/in/photostream/) (CC BY-SA 2.0)](img/college_student_computer.jpg)

#

## On the Road to Cluster Computing

## Madmax

[columns,class="row vertical-align"]

[column,class="col-xs-4"]

![](img/madmax_high.jpg)

[/column]

[column,class="col-xs-8"]

* 44 nodes

	* 2x6 cores (Sandy Bridge)
	
	* 128 GB RAM
	
	* 1 TB local drive


* 200 TB Lustre parallel file system (400 MB/s to each node)

* jobs are defined to batch system (LSF)

```
$ bsub -o hw.log -q short -n 1 echo "Hello World!"
```

[/column]

[/columns]


## The Daily Torture

[columns,class="row vertical-align"]

[column,class="col-xs-6"]

![[Sisyphus (1548–49) by Tizian](https://en.wikipedia.org/wiki/Sisyphus) (public domain)](img/600px-Punishment_sisyph.jpg)

[/column]

[column,class="col-xs-6"]

* bsub made for large (MPI driven) applications

* data-driven workflows "hard(er)" to implement

	* soon: bsub wrapped by bash scripts

	    - eventually: bsub scripts wrapped by other scripts

		- or: bash scripts generating bash scripts

**Warning: error prone, not fun, not productive!**

<!-- ![](img/slippery_floor.png) -->

[/column]

[/columns]


## Where many of us come from

<div style="font-size: 1.2em">
```
1. bsub <opts> /path/to/app-A in.ext1 out.ext2

2. bsub <opts> /path/to/app-B *.ext2 summary.ext3

3. bsub <opts> /path/to/app-C *.ext3 results.final
```
</div>

. . .

* **pipelines are everywhere**

* most of this with high influx of *.ext1 files

* more complex configurations on top (number of threads, gpus, ...)

## It would be nice to have

* lightweight

* rule based <br> (most pipelines consist of fixed steps, input is what changes)

* text based (think [version control](git-scm.org))

* easy to extend and flexible

<div style="font-size:2em;text-align: center;" class="fragment">
**[Snakemake](https://bitbucket.org/johanneskoester/snakemake/wiki/Home)**
</div>

## Snakemake

![bitbucket.org/johanneskoester/snakemake](img/snakemake_bitbucket_screenshot.png)

[columns,class="row vertical-align"]

[column,class="col-xs-6"]

* free and open-source
* written in python3
* motivated by GNU make

[/column]

[column,class="col-xs-6"]

* write `Snakefile` in Domain Specific Language
* Snakefile contains rules to evaluate

[/column]

[/columns]

## Domain Specific Language?


```
rule targets:
    input:
        'plots/dataset1.pdf', 
        'plots/dataset2.pdf'

rule plot:
    input:
        'raw/{dataset}.csv'
    output:
        'plots/{dataset}.pdf'
    shell:
        'somecommand {input} {output}'
```


* logic based on input/output files (here through pseudo-rule "targets")

* directed acyclic graph build up

* graph can be decomposed (independent/dependent tasks)

## A simple example

<center>
 <object type="image/svg+xml" data="img/simple.svg" width="1000" border="0" style="background-color: #FFFFFF;"> 
 </object>
</center>
<!-- ## A simple example -->

<!-- <object type="image/svg+xml" data="img/simple.svg" -->
<!-- width="1000" border="0" style="background-color: #FFFFFF;"> -->
<!-- </object> -->
<!-- <img width="1000" src="img/simple.svg"> -->

## A simple Snakemake file

<div style="max-height: 100%;">
```python
$ cat Snakemake
DATAFILES = ['dataset-01.dat','dataset-02.dat']
OUTPUT = [ item.replace(".dat",".zip") for item in DATAFILES ]

rule final:
    input: 'bag.tar'

rule compress:
    input:  '{name}.dat'
    output: '{name}.zip'
    shell:  'zip {output} {input}'

rule bag:
    input:  OUTPUT
    output: 'bag.tar'
    shell:  'tar cf {output} {input}'
```
</div>

## Running the Snakefile

```
$ snakemake -n -r #let's see what's going on
$ snakemake #run it
$ snakemake --dag | dot -Tpdf > dag.pdf #produce graph
```

See [`Snakefile`](https://idisk.mpi-cbg.de/~steinbac/resources/20150430/examples/Snakefile) in [examples](https://idisk.mpi-cbg.de/~steinbac/resources/20150430/examples) to this presentation!

## Features

* custom command line args can be handed over to 
```
$ snakemake -s cli_args.snake --config inputfiles="*dat"
```
* snakemake is cluster aware
```
$ snakemake --cluster "bsub -n 32"
```

	* snakemake ```params``` to decorate rules for cluster execution
```
rule:
    input:  ...
    output: ...
    params: runtime="04:00"
    shell: ...
```
```
snakemake --cluster "bsub -W {params.runtime}"
```

	* cluster specific configuration files

	* local versus batch rules

## Advanced Features

* benchmarking
```
rule benchmark_command:
    input:
        "path/to/input.{sample}.txt"
    output:
        "path/to/output.{sample}.txt"
    benchmark:
        "benchmarks/somecommand/{sample}.json"
    shell:
        "somecommand {input} {output}"
```
```
$ snakemake --benchmark-repeats <number>
```

##

* Embedded Python
```
rule compose_merge:
    input:
        expand('assembly/{sample}/transcripts.gtf', sample=SAMPLES)
    output:
        txt='assembly/assemblies.txt'
    run:
        with open(output.txt, 'w') as out:
            print(*input, sep="\n", file=out)
```

##

* Embedded R

```
from snakemake.utils import R

SOMECONSTANT = 42

rule:
    input:  ...
    output: ...
    run:
        R("""
        # Access any global/local variables with the braces notation
        sqrt({SOMECONSTANT});
        # be sure to mask braces used in R control flow by doubling them:
        if(TRUE) {{
            # do something
        }}
        """)

```

## Resources

* [good documentation](https://bitbucket.org/johanneskoester/snakemake/wiki/Documentation)

* [basic examples](https://bitbucket.org/johanneskoester/snakemake/wiki/Examples) (Cufflinks, Building a C Program, miRNA Analysis Pipeline, ...)

* [alive google groups forum](https://groups.google.com/forum/#!forum/snakemake)

* [repo with ready made snakefiles](https://bitbucket.org/johanneskoester/snakemake-workflows) (mostly bioinformatics workflows, open for contributions)

* quite some talks, papers ...

## Snakemake Summary

[columns,class="row vertical-align"]

[column,class="col-xs-6"]

* great tool (also for programming beginners)

* free and open-source

* great community

* great documentation

[/column]

[column,class="col-xs-6"]

![Bd bazaar ([FrancisTyers](https://commons.wikimedia.org/wiki/File:Bd_bazaar.jpg), CC BY-SA-3.0)](img/Bd_bazaar.jpg)

[/column]

[/columns]

But sometimes ... you need a cathedral!

#

## ![](img/spark-logo_halfinverted.png)

* cluster computing framework

* originally developed by AMPlab at University of California, Berkeley (donated to Apache Foundattion later)
<!-- * multi-stage in-memory primitives -->

* requires a cluster manager (native, Yarn, Mesos) 

* requires a distributed storage system (native, HDFS, Cassandra, Amazon S3)

![[Spark](https://spark.apache.org/) Software Stack (no license)](img/spark-stack.png)


## Spark Core = Resilient Distributed Datasets

[columns,class="row vertical-align"]

[column,class="col-xs-6"]

Architectural Motivation


 <object type="image/svg+xml" data="img/spark_rdd_fig2.svg" width="800" border="0" style="background-color: #FFFFFF;"> 
 </object>
 from ([Zaharia et al, 2012](http://people.csail.mit.edu/matei/papers/2012/nsdi_spark.pdf), figure 2)


[/column]

[column,class="col-xs-6"]

Operation Lineage

![from ([Zaharia et al, 2012](http://people.csail.mit.edu/matei/papers/2012/nsdi_spark.pdf), figure 5)](img/spark_rdd_fig5.png)

[/column]

[/columns]

## Spark Code

* spark written in Scala (JVM based multi-paradigm language)

* supports python, R and Java

* code very simple, provides primitives for most data-parallel tasks

* map-reduce with user-defined map function `my_color_image` and reducer `add`

```
from pyspark import SparkContext

sc = SparkContext(appName="PythonExample")

colorlist = sc.parallelize(my_filelist).map(my_color_image).reduce(add)

sc.stop()
```

## Spark Scalability

## Spark Summary

* clearly Spark is subject to hype right now

* integration with classical HPC systems doable, but cumbersome

* syntax is clean and easy to adapt (complexity hidden)

* no advertisement for spark here, but placeholder for good library/framework that leverages performance and developer fun

# Summary

* 

## Thank you ...

for your attention!
