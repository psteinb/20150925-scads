echo "id n_cores n_files start_epoch end_epoch duration_s" > temp.data
N_FILES=296

FILES=$@
for f in $FILES;do 
    
    ID=${f/.log/}
    NCORES=`echo ${ID}|cut -f3 -d'_'`
    STARTDATE=`egrep -i '^Started' ${f}|sed -e 's/Started at//'`;
    ENDDATE=`egrep -i '^Results reported at' ${f}|sed -e 's/Results reported at//'`;

    START_EPOCH=`date -d "${STARTDATE}" +%s`
    END_EPOCH=`date -d "${ENDDATE}" +%s`

    DELTA=`echo "${END_EPOCH}-${START_EPOCH}"|bc`
    echo -e "${ID} ${NCORES} ${N_FILES} ${START_EPOCH} ${END_EPOCH} ${DELTA}";
done|column -t >> temp.data
cat temp.data | column -t > spark_gpu.data
rm temp.data