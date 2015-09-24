echo "file start_epoch end_epoch duration_s" > temp.data

if [[ -n $1 && -d $1 ]];then
    FILEDIR=$1
else
    FILEDIR=$PWD
fi

LOGFILES=`lfs ls ${FILEDIR}/*log`
for i in ${LOGFILES};do 

    STARTDATE=`egrep -i '^Started' ${i}|sed -e 's/Started at//'`;
    ENDDATE=`egrep -i '^Results reported at' ${i}|sed -e 's/Results reported at//'`;

    START_EPOCH=`date -d "${STARTDATE}" +%s`
    END_EPOCH=`date -d "${ENDDATE}" +%s`

    DELTA=`echo "${END_EPOCH}-${START_EPOCH}"|bc`
    echo -e "${i} ${N_FILES} ${START_EPOCH} ${END_EPOCH} ${DELTA}";
done|column -t >> temp.data
cat temp.data | column -t > ${FILEDIR}/snakemake.timings.data
rm temp.data