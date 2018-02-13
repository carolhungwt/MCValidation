#!/usr/bin/env python

import argparse

def plotm4l(lhefiles, saveas, mh):
  h = ROOT.TH1F("m4l", "m_{4l}", 50, mh-100, mh+1000)  #may want to adjust these numbers
  hm1 = ROOT.TH1F("mZ1", "m_{Z1}", 25, 50, 100)
  hm2 = ROOT.TH1F("mZ2", "m_{Z2}", 25, 50, 100)
  hcostheta1 = ROOT.TH1F("costheta1", "costheta1", 25, -1, 1)
  hcostheta2 = ROOT.TH1F("costheta2", "costheta2", 25, -1, 1)
  hcosthetastar = ROOT.TH1F("costhetastar", "costhetastar", 25, -1, 1)
  hPhi = ROOT.TH1F("Phi", "Phi", 25, -10, 10)
  hPhi1 = ROOT.TH1F("Phi1", "Phi1", 25, -10, 10)
  m4lrange=[124.99,125.01]
  if mh>125:  m4lrange=[200,300]
  for lhefile in lhefiles:
    with LHEFile_MCFM(lhefile) as f:
      for event in f:
        #gives a segfault if you don't compute at least one probability...
        event.ghz1 = 1
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.computeP()
        m4l, m1, m2, costheta1, costheta2, Phi, costhetastar, Phi1 = event.computeDecayAngles()
        h.Fill(m4l)
	if m4l>m4lrange[1] or m4l<m4lrange[0]:  continue
	hm1.Fill(m1)
	hm2.Fill(m2)
	hcostheta1.Fill(costheta1)
	hcostheta2.Fill(costheta2)
	hPhi.Fill(Phi)
	hPhi1.Fill(Phi1)
	hcosthetastar.Fill(costhetastar)
	  
#  c1 = ROOT.TCanvas()
#  h.Draw()
  w = ROOT.RooWorkspace('w')
  getattr(w,'import')(h,"h",1)
  if mh<m4lrange[1] and mh>m4lrange[0]:
    getattr(w,'import')(hm1,"hm1",1)
    getattr(w,'import')(hm2,"hm2",1)
    getattr(w,'import')(hcostheta1,"hcostheta1",1)
    getattr(w,'import')(hcostheta2,"hcostheta2",1)
    getattr(w,'import')(hcosthetastar,"hcosthetastar",1)
    getattr(w,'import')(hPhi,"hPhi",1)
    getattr(w,'import')(hPhi1,"hPhi1",1)
  for filename in saveas:
    f = ROOT.TFile(filename,'recreate')
    f.WriteTObject(w)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("lhefiles", nargs="+")
  parser.add_argument('--nbin',type=int,default=100)
  parser.add_argument('--mh',type=float,default=125.)
  parser.add_argument('--range',type=float, default=0.5)
  parser.add_argument("--saveas", action="append", required=True, help="filename(s) to save results, can provide multiple times")
  args = parser.parse_args()

#put these imports at the bottom so if you do ./plotm4l.py --help it doesn't have to load them
import ROOT
from lhefile import LHEFile_MCFM
from ZZMatrixElement.MELA.mela import TVar

if __name__ == "__main__":
  plotm4l(args.lhefiles, args.saveas,args.mh)

