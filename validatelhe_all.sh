#!/usr/bin/env bash
filename=$1
mh=$2
coupling=$3
#if [ ${filename} -eq "-h" ]; then echo "filename mh nibn range"; exit 0; fi

curdir=$PWD
cmsswdir="/afs/cern.ch/user/w/wahung/CMSSW_8_0_26_patch1"
cd ${cmsswdir}
eval `scramv1 runtime -sh`
cd ${curdir}

if [[ -z ${mh} ]]; then mh=125; fi
if [[ -z ${coupling} ]]; then echo "coupling should be provided"; exit 1; fi


inputlhe=${folder}_dir/${filename}.lhe

for selection in 2016 2017; do
if [[ ${selection} -eq "2016" ]]; then inputlhe="2016_MCFM+JHUGen_sample/${coupling}/ggZZ_Sig_ELMU/HZZ_tb_lord_NNPDF30_0___0___125_ELMU__13TeV_halfmzz_4.lhe"; 
else inputlhe=${filename}_dir/${filename}.lhe; fi

./plotm4l_all.py ${inputlhe} --mh ${mh} --saveas ${filename}_lhe_${selection}.root
done
mv ${filename}_lhe_2017.root ${filename}_lhe_2016.root ${filename}_dir
./combineplots_all.py --name ${filename}

