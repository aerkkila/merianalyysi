#!/bin/bash

muuttujat=(icevolume soicecov)

ajoja=`find -type d -name "SS_ice_*" |wc -l`
for j in `seq $ajoja`; do
    echo
    echo ajo $j / $ajoja
    kansio=`find -type d -name "SS_ice_*" |head -$j |tail -1` #esim SS_ice_A001
    for tmp in ${!muuttujat[*]}
    do
	tied[tmp]=${muuttujat[tmp]}_${kansio:(-4)} #esim icevolume_A001
    done
    
    cd $kansio
    n=`ls -1 ${tied}_*.nc |wc -l`
    for i in `seq $n`; do
	for tmp in ${!muuttujat[*]}
	do
	    nimi[tmp]=`ls -1 ${tied[tmp]}_*.nc |head -$i |tail -1`
	    nimi[tmp]=${nimi[tmp]:0:(-3)} #esim icevolume_A001_1975
	    echo ${nimi[tmp]}
	    ncdump -v ${muuttujat[tmp]} ${nimi[tmp]}.nc |sed -n "/${muuttujat[tmp]} =/,\$p" > ../ncteksti/${nimi[tmp]}.txt
	done
    done
    cd ..
done
