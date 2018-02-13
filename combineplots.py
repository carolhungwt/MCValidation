#!/usr/bin/env python
import argparse
import ROOT as root

def makeplot(lhename,xrdname,plotname):
  c = root.TCanvas()
  flhe = root.TFile.Open(lhename)
  try:
    wlhe = flhe.Get('w')
    hlhe = wlhe.obj('h')
    hlhe.SetLineColor(2)
    hlhe.SetLineColor(2)
    hlhe.GetYaxis().SetLimits(0.,0.5)
    fxrd = root.TFile.Open(xrdname)
    wxrd = fxrd.Get('w')
    hxrd = wxrd.obj('h')
    hxrd.SetLineColor(1)
    hxrd.SetLineWidth(2)
    hxrd.GetYaxis().SetLimits(0.,0.5)
    c.cd()

    hlhe.DrawNormalized('')
    hxrd.DrawNormalized('same')
    c.SaveAs(plotname)
  except Exception as e:
    print e
    pass

parser = argparse.ArgumentParser()
parser.add_argument('--lhe')#,required=True)
parser.add_argument('--xrd')#,required=True)
parser.add_argument('--saveas',default='~/www/combinedplot.png')
parser.add_argument('--names',action='append')
args = parser.parse_args()

if args.names:
  for name in args.names:
    lhename = name+'_dir/'+name+'_lhe.root'
    xrdname = name+'_dir/'+name+'_xrd.root'
    plotname = '~/www/MCFM+JHUGen_MC_Validation/'+name+'.png'
    makeplot(lhename,xrdname,plotname) 
else:
    lhename = args.lhe
    xrdname = args.xrd
    plotname = args.saveas
    makeplot(lhename,xrdname,plotname)
