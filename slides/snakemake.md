% Snakemake 
% Peter Steinbach, steinbac@mpi-cbg
% April 30, 2015


<section data-background="images/house_of_cards_1024.jpeg">

<div style="margin-top: 2%;margin-bottom: 80%;">
<h1>Status Quo ?</h1>
</div>

## Where many of us come from

<div style="font-size: 1.2em">
```
1. bjobs <opts> /path/to/app-A in.ext1 out.ext2

2. bjobs <opts> /path/to/app-B *.ext2 summary.ext3

3. bjobs <opts> /path/to/app-C *.ext3 results.final
```
</div>

. . .

* **pipelines are everywhere**

* most of this with high influx of *.ext1 files

* more complex configurations on top (number of threads, gpus, ...)

* shell scripts error prone (especially for beginners)


## It would be nice to have

* lightweight

* rule based <br> (most pipelines consist of fixed steps, input is what changes)

* text based (think [version control][git-vcs])

* easy to extend and flexible

<div style="font-size:2em" class="fragment">
**[Snakemake](https://bitbucket.org/johanneskoester/snakemake/wiki/Home)**
</div>

</section>


# Snakemake

## A Scalable workflow engine

![bitbucket.org/johanneskoester/snakemake](images/snakemake_bitbucket_screenshot.png)

<div style="width: 45%;float: left">
* free and open-source
* written in python3
* motivated by GNU make
</div>

<div style="width: 45%;float: right">
* write `Snakefile` in Domain Specific Language
* Snakefile contains rules to evaluate
</div>

## Domain Specific Language

<div style="width: 80%;font-size: 1.3em;">
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
</div>


* logic based on input/output files (here through pseudo-rule "targets")
* directed acyclic graph build up
* graph can be decomposed (independent/dependent tasks)

## A simple example

<img width="1000" src="images/simple.svg">

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

. . .
```
$ snakemake -n -r #let's see what's going on
$ snakemake #run it
$ snakemake --dag | dot -Tpdf > dag.pdf #produce graph
```

See [`Snakefile`](https://idisk.mpi-cbg.de/~steinbac/resources/20150430/examples/Snakefile) in [examples](https://idisk.mpi-cbg.de/~steinbac/resources/20150430/examples) to this presentation!

## *Let's run it!* ##

## Respawning

### See example [`respawn.snake`](https://idisk.mpi-cbg.de/~steinbac/resources/20150430/examples/respawn.snake)

```
$ snakemake -s respawn.snake --config inputfiles="*dat"
```


## Command Line args

### See example [`cli_args.snake`](https://idisk.mpi-cbg.de/~steinbac/resources/20150430/examples/cli_args.snake)

```
$ snakemake -s cli_args.snake --config inputfiles="*dat"
```

## Cluster support

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
* snakemake can use [DRMAA API][wikiDRMAA] as interface to batch system
```
$ snakemake --drmaa " -q short" -j 32
```
* cluster specific configuration files
* local versus batch rules

# Advanced Topics

## Benchmarking

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

* will produce json file for further processing

## Embedded Python
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
taken from [Cufflinks Example](https://bitbucket.org/johanneskoester/snakemake/wiki/Examples)

## Embedded R

```
rom snakemake.utils import R

SOMECONSTANT = 42

rule:
    input:  ...
    output: ...
    run:
        R("""
        # Access any global or local variables from the Snakefile with the braces notation
        sqrt({SOMECONSTANT});
        # be sure to mask braces used in R control flow by doubling them:
        if(TRUE) {{
            # do something
        }}
        """)

```

## Reporting

```
from snakemake.utils import report

SOMECONSTANT = 42

rule report:
    input:  F1="someplot.pdf",
            T1="sometable.txt"
    output: html="report.html"
    run:
        report("""
        =======================
        The title of the report
        =======================

        Write your report here, explaining your results. Don't fear to use math, 
        it will be rendered correctly in any browser using MathJAX, 
        e.g. inline :math:`\sum_{{j \in E}} t_j \leq I`, 
        or even properly separated:

        .. math::

            |cq_{{0ctrl}}^i - cq_{{nt}}^i| > 0.5

        Include your files using their keyword name and an underscore: F1_, T1_.

        Access your global and local variables like within shell commands, e.g. {SOMECONSTANT}.
        """, output.html, metadata="Johannes Köster (johannes.koester@uni-due.de)", **input)
```

## Resources

* [good documentation](https://bitbucket.org/johanneskoester/snakemake/wiki/Documentation)
* [basic examples](https://bitbucket.org/johanneskoester/snakemake/wiki/Examples) (Cufflinks, Building a C Program, miRNA Analysis Pipeline, ...)
* [alive google groups forum](https://groups.google.com/forum/#!forum/snakemake)
* [repo with ready made snakefiles](https://bitbucket.org/johanneskoester/snakemake-workflows) (mostly bioinformatics workflows, open for contributions)
* quite some talks, papers ...

# Summary

## Snakemake

* young open-source project
* readable syntax (scriptable with python, R, ...)
* scales on cluster as well as on laptop
* multi-process job resolution dispatch from directed acyclic graph
* offers much more features than I could have covered

<div style="font-size:2em" class="fragment">
**[Snakemake](https://bitbucket.org/johanneskoester/snakemake/wiki/Home)**
</div>

[git-vcs]: https://git-scm.com "git vcs"
[wikiDRMAA]: https://en.wikipedia.org/wiki/DRMAA "wikipedia DRMAA page"

