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
skimmedTree = TChain("test/tree_")

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


#    print "\n*****\nWARNING: *Test run* Processing 200 events only.\n*****\n"
#    for ievent in range(200):
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

            #caloMet                      = skimmedTree.__getattr__('CaloMET')
	    pfrawMET                     = skimmedTree.__getattr__('pfrawMET')
            #isData                     = skimmedTree.__getattr__('isData')

        except Exception as e:
            print e
            print "Corrupt file detected! Skipping 1 event."
            continue

        trigstatus=False



        trigger1=False; trigger2=False


	#print "len of trigger status:  ",len(trigResult)

	'''
	for i in range(len(trigResult)):
		#print "trigger status", bool(trigResult[i])
		print "trigger name:   ", str(trigName[i])
		print "trigger status:   ", bool(trigResult[i])
        '''
 
	#print "Calo MET", caloMet,  "pfrawMET", pfrawMET
	
        trigger1 = CheckFilter(trigName, trigResult, 'HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned_v')
	trigger2 = CheckFilter(trigName, trigResult,'HLT_PFMET120_PFMHT120_IDTight_v')
        if trigger1:
	    trigstatus=True
	    count+=1


	#if trigstatus: print "+++++++++++++++++++++++++++++"

	'''
        trigstatus_mu=False
        trigstatus_e =False

        for itrig in range(len(triglist_e)):
            exec(triglist_e[itrig]+" = CheckFilter(trigName, trigResult, " + "'" + triglist_e[itrig] + "')")        #Runs the above commented-off code dynamically.
            exec("if "+triglist_e[itrig]+": trigstatus_e=True")                       


        for itrig in range(len(triglist_mu)):
            exec(triglist_mu[itrig]+" = CheckFilter(trigName, trigResult, " + "'" + triglist_mu[itrig] + "')")        #Runs the above commented-off code dynamically.
            exec("if "+triglist_mu[itrig]+": trigstatus_mu=True")

        for itrig in range(len(triglist)):
            exec(triglist[itrig]+" = CheckFilter(trigName, trigResult, " + "'" + triglist[itrig] + "')")        #Runs the above commented-off code dynamically.
            exec("if "+triglist[itrig]+": trigstatus=True")
        
        filterstatus = False
        filter1 = False; filter2 = False;filter3 = False;filter4 = False; filter5 = False; filter6 = False; filter7 =False; filter8 = False
        ifilter_=0
        filter1 = CheckFilter(filterName, filterResult, 'Flag_HBHENoiseFilter')
        filter2 = CheckFilter(filterName, filterResult, 'Flag_globalSuperTightHalo2016Filter')
        filter3 = CheckFilter(filterName, filterResult, 'Flag_eeBadScFilter')
        filter4 = CheckFilter(filterName, filterResult, 'Flag_goodVertices')
        filter5 = CheckFilter(filterName, filterResult, 'Flag_EcalDeadCellTriggerPrimitiveFilter')
        filter6 = CheckFilter(filterName, filterResult, 'Flag_BadPFMuonFilter')
        filter7 = CheckFilter(filterName, filterResult, 'Flag_BadChargedCandidateFilter')

        filter8 = CheckFilter(filterName, filterResult, 'Flag_HBHENoiseIsoFilter')

	filter9  =  hlt_filterbadChCandidate
	filter10 =   hlt_filterbadPFMuon
	filter11 =   hlt_filterbadGlobalMuon
	filter12 =   hlt_filtercloneGlobalMuon


        if not isData:
	        filterstatus = True
        if isData:
        	filterstatus = filter1 & filter2 & filter3 & filter4 & filter5 & filter6 & filter7 & filter8 & filter9 & filter10 & filter11 & filter12
        if filterstatus == False: continue

        jetCond=False
        muonCond=False
        eleCond=False
        ## Electron selection
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''

# append variable to fill histograms

        regquants=AllVariables.getAll()

        for quant in regquants:
            exec("allquantities."+quant+" = None")


# without any selections
	
        if trigstatus:
            allquantities.num_pf = pfrawMET
	 #   allquantities.num_calo = caloMet

        if trigstatus or not trigstatus:
            allquantities.den_pf = pfrawMET
	  #  allquantities.den_calo = caloMet
	


#Fill all the Histograms
        allquantities.FillHisto()

    allquantities.WriteHisto()
    print "Total passed events", count, "  outof ",NEntries
    print "ROOT file written to", outfilename

    print "Completed."

        # outTree.Fill()
#here your main fuction end
    # h_total_mcweight.Write()
    # h_total.Write()
    # samplepath.Write()
    # outfile.Write()




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
