#!/usr/bin/env bash
filename=$1
mh=$2
nbin=$3
range=$4
folder=$5
#if [ ${filename} -eq "-h" ]; then echo "filename mh nibn range"; exit 0; fi

if [[ -z ${mh} ]]; then mh=125; fi
if [[ -z ${nbin} ]]; then nbin=100; fi
if [[ -z ${range} ]]; then range=0.5; fi
if [[ -z ${folder} ]]; then folder="./"; fi

#echo ${filename}+${nbin}+${range}
./makeplot.py --input ${folder}/${filename}.root --nbin ${nbin} --range ${range} --mh ${mh}
./plotm4l.py ${folder}/${filename}.lhe --nbin ${nbin} --range ${range} --mh ${mh} --saveas ${filename}_lhe.root
mv ${filename}_lhe.root ${filename}_xrd.root ${filename}_dir
./combineplots.py --name ${filename}

echo "DONE" > ${filename}_DONE
