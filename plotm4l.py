#!/usr/bin/env python

import argparse

def plotm4l(lhefiles, saveas, mh, x_range, nbin):
  h = ROOT.TH1F("m4l", "m_{4l}", nbin, mh-100, mh+1000)  #may want to adjust these numbers
  for lhefile in lhefiles:
    with LHEFile_MCFM(lhefile) as f:
      for event in f:
        #gives a segfault if you don't compute at least one probability...
        event.ghz1 = 1
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.computeP()
        m4l, m1, m2, costheta1, costheta2, Phi, costhetastar, Phi1 = event.computeDecayAngles()
        h.Fill(m4l)
#  c1 = ROOT.TCanvas()
#  h.Draw()
  w = ROOT.RooWorkspace('w')
  getattr(w,'import')(h,"h",1)
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
  plotm4l(args.lhefiles, args.saveas,args.mh,args.range,args.nbin)

