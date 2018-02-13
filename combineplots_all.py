#!/usr/bin/env python
import argparse, os
import ROOT as root

hs = ['h','hm1','hm2','hcostheta1','hcostheta2','hcosthetastar','hPhi','hPhi1']

parser = argparse.ArgumentParser()
parser.add_argument('--saveas',default='~/www/combinedplot.png')
parser.add_argument('--names',action='append')
args = parser.parse_args()

for name in args.names:
  if name:
    lhename = name+'_dir/'+name+'_lhe_2017.root'
    xrdname = name+'_dir/'+name+'_lhe_2016.root'
  else:
    lhename = args.lhe
    xrdname = args.xrd
    plotname = args.saveas

  c = root.TCanvas()
  flhe = root.TFile.Open(lhename)
  fxrd = root.TFile.Open(xrdname)
  wlhe = flhe.Get('w')
  wxrd = fxrd.Get('w')

  os.system('mkdir -p ~/www/MCFM+JHUGen_MC_Validation/{name}_all/; cp ~/index.php ~/www/MCFM+JHUGen_MC_Validation/{name}_all/'.format(name=name))
  for h in hs:
    try:  
      plotname = '~/www/MCFM+JHUGen_MC_Validation/'+name+'_all/'+name+'_'+h+'.png'
      hlhe = wlhe.obj(h)
      hlhe.SetLineColor(2)
      hlhe.SetLineColor(2)
      hlhe.GetYaxis().SetLimits(0.,0.5)
      hxrd = wxrd.obj(h)
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

