echo "type n_cores n_files start_epoch end_epoch duration_s" > temp.data

for i in `seq 156 -12 12`;do 


    N_FILES=`lfs find /projects/hpcsupport/steinbac/scads/snakemake/run_${i}_jobs -type l|wc -l`
##Snakefile was symlinked in as well
    N_FILES=$((N_FILES-1))

    
    STARTDATE=`egrep -i '^Started' snakemake_${i}jobs*_first.log|sed -e 's/Started at//'`;
    ENDDATE=`egrep -i '^Results reported at' snakemake_${i}jobs*_last.log|sed -e 's/Results reported at//'`;

    START_EPOCH=`date -d "${STARTDATE}" +%s`
    END_EPOCH=`date -d "${ENDDATE}" +%s`

    DELTA=`echo "${END_EPOCH}-${START_EPOCH}"|bc`
    echo -e "snakemake ${i} ${N_FILES} ${START_EPOCH} ${END_EPOCH} ${DELTA}";
done|column -t >> temp.data
cat temp.data | column -t > snakemake.data
rm temp.data