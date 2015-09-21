for i in `seq 156 -12 12`;do 
    STARTDATE=`egrep -i '^Started' snakemake_${i}jobs*_first.log|sed -e 's/Started at//'`;
    ENDDATE=`egrep -i '^Results reported at' snakemake_${i}jobs*_last.log|sed -e 's/Results reported at//'`;
    echo -e "snakemake ${i}" `date -d "$STARTDATE" +%s` `date -d "${ENDDATE}" +%s`;
done|column -t > snakemake.data