#!/usr/bin/env python2

class scriptclass(object):
	def __init__(self,finalstate,signalbkgbsi,coupling,width):
		self.coupling = coupling
		self.signalbkgbsi = signalbkgbsi
		self.finalstate = finalstate
		self.width = width

	def submit(self):
		assert os.path.exists(self.subscriptfilename)
		os.system('chmod 755 '+self.subscriptfilename)
		subprocess.check_call(['bsub','-q','1nd',self.subscriptfilename])

	def writesubmissionscript(self):
		with open(self.subscriptfilename,'w') as fout:
			substr='#!/bin/bash\n'
			substr+='cmsswdir=/afs/cern.ch/user/w/wahung/CMSSW_8_0_26_patch1\n'	
			substr+='workdir={workdir}\n'.format(workdir=self.workdir)
#			substr+=self.untarscript
			substr+='cd ${cmsswdir}\neval `scramv1 runtime -sh`\n'
			substr+='cd ${workdir}\n'
			substr+=self.dnfromxrdscript
			substr+='mv {bashtag}.root {bashtag}_dir\n'.format(bashtag=self.bashtag)
			substr+='./validatelhe.sh {bashtag} 125 50 0.5 {bashtag}_dir\n'.format(bashtag=self.bashtag)
#			substr+='if [ ! -z "{bashtag}_DONE" ]; then mkdir -p {bashtag}_dir; mv {bashtag}* {bashtag}_dir; fi\n'.format(bashtag=self.bashtag)
#			substr+='rm -rf {bashtag}_dir\n'.format(bashtag=self.bashtag)
			fout.write(substr)

	@property 
	def workdir(self):
	  return "/afs/cern.ch/user/w/wahung/work/public/CMSSW_8_0_26_patch1/src/MC_check_from_Heshy"

	@property
	def subscriptfilename(self):
		return self.bashtag+'_submit.sh'

	@property
	def dnfromxrdscript(self):
		tmpstr = 'xrdcp root://lxcms03//data3/Higgs/170623/{bashtag}/ZZ4lAnalysis.root {bashtag}.root\n'.format(bashtag=self.bashtag)
		return tmpstr 

	@property 
	def identifier(self):
		return [self.finalstate,self.signalbkgbsi,self.coupling,self.width]

	@property
	def untarscript(self):
		if not os.path.exists(self.gridpackloc):
		  print self.gridpackloc
		  raise OSError(''.join(self.dentifier)+' gridpack not found')
		tmpstr = 'cd $(mktemp -d); cp {gridpackloc} .; tar xzvf *.tgz \n'.format(gridpackloc=self.gridpackloc)
		tmpstr+= "sed -i '72i\ cp cmsgrid_final.lhe {workdir}/{bashtag}.lhe' runcmsgrid.sh\n".format(bashtag=self.bashtag, workdir=self.workdir) 
		tmpstr+= "./runcmsgrid.sh 2000 {randseed} 12\n".format(randseed=random.randint(50000,500000))
		return tmpstr

	@property
	def signalbkgbsitag(self):
		if self.signalbkgbsi == 'SIG':		return ''
		else:					return 'Contin'

	@property
	def bashtag(self):
		if int(self.width) == 1:
		#ggTo4e_0PMH125_MCFM701
		  return 'ggTo{finalstate}_{coupling}H125{signalbkgbsitag}_MCFM701'.format(coupling=self.coupling,finalstate=self.finalstate,signalbkgbsitag=self.signalbkgbsitag)
		else:
		#ggTo4tau_0Mf05ph0H125Contin_10GaSM_MCFM701
		  return 'ggTo{finalstate}_{coupling}H125{signalbkgbsitag}_{width}GaSM_MCFM701'.format(finalstate=self.finalstate,coupling=self.coupling,width=self.width,signalbkgbsitag=self.signalbkgbsitag)

	@property
	def widthtag(self):
		if int(self.width) == 1:	return ''
		else:				return self.width

	@property
	def gridpackloc(self):
		#MCFM_mdata_slc6_amd64_gcc630_CMSSW_9_3_0_GluGluToHiggs0PMcontinToZZTo4e_M125_10GaSM_13TeV_MCFM701_pythia8
		v=3
		tmploc = '/afs/cern.ch/user/w/wahung/work/public/CMSSW_9_3_0/src/makegridpacks/gridpacks/2017/13TeV/mcfm/MCFM_mdata_slc6_amd64_gcc630_CMSSW_9_3_0_GluGluToHiggs{coupling}{signaltaglower}ToZZTo{finalstate}_M125_{widthtag}GaSM_13TeV_MCFM701_pythia8/v{v}/MCFM_mdata_slc6_amd64_gcc630_CMSSW_9_3_0_GluGluToHiggs{coupling}{signaltaglower}ToZZTo{finalstate}_M125_{widthtag}GaSM_13TeV_MCFM701_pythia8.tgz'.format(coupling=self.coupling,finalstate=self.finalstate,widthtag=self.widthtag,signaltaglower=self.signalbkgbsitag.lower(),v=v)
		if not os.path.exists(tmploc):	
		  v=2
		  tmploc = '/afs/cern.ch/user/w/wahung/work/public/CMSSW_9_3_0/src/makegridpacks/gridpacks/2017/13TeV/mcfm/MCFM_mdata_slc6_amd64_gcc630_CMSSW_9_3_0_GluGluToHiggs{coupling}{signaltaglower}ToZZTo{finalstate}_M125_{widthtag}GaSM_13TeV_MCFM701_pythia8/v{v}/MCFM_mdata_slc6_amd64_gcc630_CMSSW_9_3_0_GluGluToHiggs{coupling}{signaltaglower}ToZZTo{finalstate}_M125_{widthtag}GaSM_13TeV_MCFM701_pythia8.tgz'.format(coupling=self.coupling,finalstate=self.finalstate,widthtag=self.widthtag,signaltaglower=self.signalbkgbsitag.lower(),v=v)
		return tmploc

def jobexists(jobsubmitscript):
	output = subprocess.check_output(['bjobs','-w'],stderr=subprocess.STDOUT)
	jid=0
	for line in output.split('\n'):
		if jobsubmitscript in line:
			line = line.split()
			jid = line[0]
			return True,jid
	return False,jid

def makeratioplot(scriptcls):
  assert type(scriptcls) == scriptclass
  if scriptcls.coupling == '0PM': return
  smobj = scriptclass(scriptcls.finalstate,scriptcls.signalbkgbsi,"0PM",width)
  if not os.path.exists(os.path.join(smobj.bashtag+"_dir",smobj.bashtag+'_lhe.root')):  
    print "OPM obj not ready for ratio plot yet"
    return
#  if os.path.exists('~/www/MCFM+JHUGen_MC_Validation/ratioplot/ratioplot_'+scriptcls.bashtag+'.png'):  return 
  cmd =['./ratio_combineplots.py','--coupling',scriptcls.coupling,'--bsi',scriptcls.signalbkgbsi,'--fs',scriptcls.finalstate,'--width',scriptcls.width]
  FNULL = open(os.devnull, 'w')
  print ' '.join(cmd)
#  print 'making ratio plot'
  subprocess.Popen(cmd, stderr=subprocess.STDOUT,stdout=FNULL)

def validateall(scriptcls):
  mh = map(str,[125, 200])
  assert type(scriptcls) == scriptclass
  print "validating 2016 and 2017 all vars"
  cmd = ['./validatelhe_all.sh',scriptcls.bashtag,mh[0],scriptcls.coupling]
  print ' '.join(cmd)
  FNULL = open(os.devnull, 'w')
#  subprocess.Popen(cmd, stderr=subprocess.STDOUT,stdout=FNULL)


import random, subprocess, os
if __name__=="__main__":
  needratio = 1
  needvalidateall=1
  couplings = ["0PM", "0PH", "0PHf05ph0", "0PL1", "0PL1f05ph0", "0M", "0Mf05ph0"]
  signalbkgbsis = ["SIG"]#,"BSI"]
  widths = ['1']
  finalstate = ['2e2mu']
  for signalbkgbsi in signalbkgbsis:
	for coupling in couplings:
	  for fs in finalstate:
	    for width in widths:
		tmpobj = scriptclass(fs,signalbkgbsi,coupling,width)

		if needvalidateall:  
		  validateall(tmpobj)
		  continue

		print ' '.join(map(str,tmpobj.identifier))
		if not os.path.exists(tmpobj.gridpackloc):		
		  print tmpobj.bashtag+" gridpack not ready"
		  continue
		if os.path.exists('/afs/cern.ch/user/w/wahung/www/MCFM+JHUGen_MC_Validation/{bashtag}.png'.format(bashtag=tmpobj.bashtag)):
#		  if os.path.exists('{bashtag}_dir/{bashtag}.root'.format(bashtag=tmpobj.bashtag)):
#		    os.system('rm {bashtag}_dir/{bashtag}.root'.format(bashtag=tmpobj.bashtag))
		  if needratio:  makeratioplot(tmpobj)
		  print "{bashtag}.png already exists".format(bashtag=tmpobj.bashtag)
		  continue
		if os.path.exists('{bashtag}_dir'.format(bashtag=tmpobj.bashtag)):
		  print "{bashtag}_dir ready but no png yet".format(bashtag=tmpobj.bashtag)
		  print 'making png'
		  subprocess.Popen(['./combineplots.py','--name',tmpobj.bashtag])
		  continue
		jobrunning, jid = jobexists(tmpobj.subscriptfilename)
		if jobrunning:
		  print 'job running with jobid {jid}'.format(jid=jid)
		  continue
		print tmpobj.bashtag+" submitting validation"
		tmpobj.writesubmissionscript()
		tmpobj.submit()
