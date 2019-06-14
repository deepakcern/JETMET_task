#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math
import AllVariables
from AllHists import *


ROOT.gROOT.SetBatch(True)

ROOT.gROOT.LoadMacro("Loader.h+")

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)


parser.add_option("-i", "--inputfile",  dest="inputfile")
parser.add_option("-o", "--outputfile", dest="outputfile")
parser.add_option("-D", "--outputdir", dest="outputdir")
parser.add_option("-F", "--farmout", action="store_true",  dest="farmout")

(options, args) = parser.parse_args()


if options.farmout==None:
    isfarmout = False
else:
    isfarmout = options.farmout


inputfilename = options.inputfile
outputdir = options.outputdir


pathlist = inputfilename.split("/")
sizeoflist = len(pathlist)
#print ('sizeoflist = ',sizeoflist)
rootfile='tmphist'
rootfile = pathlist[sizeoflist-1]
textfile = rootfile+".txt"

if outputdir!='.': os.system('mkdir -p '+outputdir)

if options.outputfile is None or options.outputfile==rootfile:
    if not isfarmout:
        outputfilename = "/Output_"+rootfile
    else:
        outputfilename = "/Output_"+rootfile.split('.')[0]+".root"
else:
    outputfilename = "/"+options.outputfile



outfilename = outputdir + outputfilename
#else:
#    outfilename = options.outputfile

print "Input:",options.inputfile, "; Output:", outfilename


#outfilename= 'SkimmedTree.root'
skimmedTree = TChain("hltJetMetNtuple/tree_")

if isfarmout:
    infile = open(inputfilename)
    failcount=0
    for ifile in infile:
        try:
            f_tmp = TFile.Open(ifile.rstrip(),'READ')
            if f_tmp.IsZombie():            # or fileIsCorr(ifile.rstrip()):
                failcount += 1
                continue
            skimmedTree.Add(ifile.rstrip())
        except:
            failcount += 1
    if failcount>0: print "Could not read %d files. Skipping them." %failcount

if not isfarmout:
    skimmedTree.Add(inputfilename)


#
# skimmedTree.Add(sys.argv[1])

def arctan(x,y):
    corr=0
    if (x>0 and y>=0) or (x>0 and y<0):
        corr=0
    elif x<0 and y>=0:
        corr=math.pi
    elif x<0 and y<0:
        corr=-math.pi
    if x!=0.:
        return math.atan(y/x)+corr
    else:
        return math.pi/2+corr

def getPT(P4):
    return P4.Pt()


def AnalyzeDataSet():


    allquantities = trigeerTurnOn(outfilename)
    allquantities.defineHisto()

    
    '''
    triglist=['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v','HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v']
   
    trig_1=['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v']
    trig_2=['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v']
    trig_3=['HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v']

    triglist_mu=['HLT_IsoMu27_v']
    triglist_e = ['HLT_Ele27_WPTight_Gsf']
    '''
    outfile = TFile(outfilename,'RECREATE')
    #
    # outTree = TTree( 'outTree', 'tree branches' )
    # samplepath = TNamed('samplepath', str(sys.argv[1]))

    NEntries = skimmedTree.GetEntries()
    #NEntries = 1000
    print 'NEntries = '+str(NEntries)
    npass = 0
    count = 0
    for ievent in range(NEntries):
        if ievent%100==0: print "Processed "+str(ievent)+" of "+str(NEntries)+" events."
        skimmedTree.GetEntry(ievent)
        ## Get all relevant branches
        try:

    #        run                        = skimmedTree.__getattr__('runId')
    #        lumi                       = skimmedTree.__getattr__('lumiSection')
    #        event                      = skimmedTree.__getattr__('eventId')
    #        print "Run:"+str(run)+"; Lumi:"+str(lumi)+"; Event:"+str(event)
            trigName                   = skimmedTree.__getattr__('trigName')
            trigResult                 = skimmedTree.__getattr__('trigResult')
            #filterName                 = skimmedTree.__getattr__('hlt_filterName')
            #filterResult               = skimmedTree.__getattr__('hlt_filterResult')
            muonE                      = skimmedTree.__getattr__('muonE')
	#    if len(muonE)!=0:continue
            caloMet                      = skimmedTree.__getattr__('CaloMET')
	    pfrawMET                     = skimmedTree.__getattr__('pfrawMET')
            #isData                     = skimmedTree.__getattr__('isData')

        except Exception as e:
            print e
            print "Corrupt file detected! Skipping 1 event."
            continue

        trigstatus=False; trigger1=False; trigger2=False	
        trigger1 = CheckFilter(trigName, trigResult, 'HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned_v')
	trigger2 = CheckFilter(trigName, trigResult,'HLT_PFMET120_PFMHT120_IDTight_v')
        if trigger1:
	    trigstatus=True
	    #count+=1

        MuonCond=False
        if len(muonE)==0:
            MuonCond=True


# append variable to fill histograms

        regquants=AllVariables.getAll()

        for quant in regquants:
            exec("allquantities."+quant+" = None")


# fill histogram
	
        if trigstatus and MuonCond:
            allquantities.num_pf = pfrawMET
	    allquantities.num_calo = caloMet

        if MuonCond:
            allquantities.den_pf = pfrawMET
	    allquantities.den_calo = caloMet
	


#Fill all the Histograms
        allquantities.FillHisto()

    allquantities.WriteHisto()
    print "ROOT file written to", outfilename

    print "Completed."

        # outTree.Fill()


def CheckFilter(filterName, filterResult,filtercompare):
    ifilter_=0
    filter1 = False
    for ifilter in filterName:
        filter1 = (ifilter.find(filtercompare) != -1)  & (bool(filterResult[ifilter_]) == True)
        if filter1: break
        ifilter_ = ifilter_ + 1
    return filter1

def DeltaR(p4_1, p4_2):
    eta1 = p4_1.Eta()
    eta2 = p4_2.Eta()
    eta = eta1 - eta2
    eta_2 = eta * eta

    phi1 = p4_1.Phi()
    phi2 = p4_2.Phi()
    phi = Phi_mpi_pi(phi1-phi2)
    phi_2 = phi * phi

    return math.sqrt(eta_2 + phi_2)

def Phi_mpi_pi(x):
    kPI = 3.14159265358979323846
    kTWOPI = 2 * kPI

    while (x >= kPI): x = x - kTWOPI;
    while (x < -kPI): x = x + kTWOPI;
    return x;

def DeltaPhi(phi1,phi2):
   phi = Phi_mpi_pi(phi1-phi2)

   return abs(phi)

def CheckFilter(filterName, filterResult,filtercompare):
    ifilter_=0
    filter1 = False
    for ifilter in filterName:
        filter1 = (ifilter.find(filtercompare) != -1)  & (bool(filterResult[ifilter_]) == True)
        if filter1: break
        ifilter_ = ifilter_ + 1
    return filter1



def MT(Pt, met, dphi):
    return ROOT.TMath.Sqrt( 2 * Pt * met * (1.0 - ROOT.TMath.Cos(dphi)) )

if __name__ == "__main__":
    AnalyzeDataSet()
