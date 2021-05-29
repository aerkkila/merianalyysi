#!/bin/bash

kansio0=`pwd`
cd ~/Lataukset
if [ $? -ne 0 ]
then
    return 1
fi

for nimi in `ls SS_ice_*.zip`
do
    kansio=${nimi:0:(-4)}
    polku=${kansio0}/${kansio}
    mkdir ${polku}
    unzip ${kansio} -x *velo* *snow* -d ${polku}
done
