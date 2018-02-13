#!/usr/bin/env python
import argparse,sys,numpy
import ROOT as root
from preparelhexrd import scriptclass

parser = argparse.ArgumentParser()
parser.add_argument('--fs' , help='final states',type=str)
parser.add_argument('--bsi',help='bsi or sig or bkg',type=str)
parser.add_argument('-w','--width',help='1 or 10 or 25',type=str)
parser.add_argument('-c','--coupling',type=str)
parser.add_argument('--nbin',default=100,type=int)
parser.add_argument('--mh',type=int,default=125)
args = parser.parse_args()

coupling, fs, signalbkgbsi = args.coupling, args.fs, args.bsi

smobj = scriptclass(fs,signalbkgbsi,'0PM',args.width)
sigobj = scriptclass(fs,signalbkgbsi,coupling,args.width)

#ratiohist = root.TH1F(sigobj.bashtag,sigobj.bashtag,args.nibin,args.mh-100,args.mh+1000)
try:
    smname = smobj.bashtag+'_dir/'+smobj.bashtag+'_lhe.root'
    signame = sigobj.bashtag+'_dir/'+sigobj.bashtag+'_lhe.root'
    plotname = '~/www/MCFM+JHUGen_MC_Validation/ratioplot/ratioplot_'+sigobj.bashtag+'.png'

    c = root.TCanvas()
    c.Divide(1,2)
    fsm = root.TFile.Open(smname)
except IOError as e:
    print e
    sys.exit()
try:
    wsm = fsm.Get('w')
    hsm = wsm.obj('h')
    hsm.SetLineColor(1)
    hsm.SetLineWidth(2) 
    fsig = root.TFile.Open(signame)
    wsig = fsig.Get('w')
    hsig = wsig.obj('h')
    hsig.SetLineColor(2)
    hsig.SetLineWidth(2)

    c.cd(1)
    hsm.DrawNormalized('histo')
    hsig.DrawNormalized('same')
 
    hratio = hsm.Clone(sigobj.bashtag+'/'+smobj.bashtag)
    hratio.SetStats(0)
    hratio.Sumw2()
    hratio.Divide(hsig)
    bin125 = hratio.FindBin(125)
    scalef = hratio.GetBinContent(bin125)
    print bin125, scalef
    for i in range(hratio.GetXaxis().GetFirst(),hratio.GetXaxis().GetLast()+1):
      tmpval = hratio.GetBinContent(i)
      if tmpval==0: hratio.SetBinContent(i,0)
      else:
        tmpval = numpy.log(tmpval/scalef) 
        hratio.SetBinContent(i,tmpval)

    hratio.SetMarkerStyle(21)
    c.cd(2)
    p2 = root.TPad()
    #hratio.GetYaxis().SetRangeUser(0,10)
    hratio.Draw("ep")
    one = root.TF1('one','0',25,1125)
    one.SetLineWidth(2)
    one.SetLineColor(2)
    one.SetLineStyle(9)
    one.Draw('same')

    c.SaveAs(plotname)
except Exception as e:
    print "ratio plot for "+sigobj.bashtag+' not done'
    print e
    quit()
