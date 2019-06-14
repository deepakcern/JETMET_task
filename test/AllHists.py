from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TH2F
import ROOT as ROOT
import AllVariables

class trigeerTurnOn:

    def __init__(self, rootfilename):

        allquantlist=AllVariables.getAll()

        for quant in allquantlist:
            exec("self."+quant+" = None")
            exec("self.h_"+quant+" = []")

        self.rootfilename = rootfilename

        self.weight   = 1.0


    def defineHisto(self):
        allquantlist=AllVariables.getAll()

        def getBins(quant):
            if 'full' in quant:
                bins='2000'
                low='0'
                high='2000'
            elif 'fract' in quant:
                bins='2000'
                low='0'
                high='2000'
            else:                   # for pT, mass, etc.
                bins='2000'
                low='0.'
                high='2000.'

            return bins,low,high

        for quant in allquantlist:
            bins,low,high=getBins(quant)
            exec("self.h_"+quant+".append(TH1F('h_"+quant+"_','h_"+quant+"_',"+bins+","+low+","+high+"))")

        print "Histograms defined"


    def FillHisto(self):
        self.weight = 1
        WF = self.weight

        allquantlist=AllVariables.getAll()
        for quant in allquantlist:
            exec("if self."+quant+" is not None: self.h_"+quant+"[0] .Fill(self."+quant+", WF)")


    def WriteHisto(self):
        f = TFile(self.rootfilename,'RECREATE')
        print
        f.cd()
        
        allquantlist=AllVariables.getAll()


        for quant in allquantlist:
            exec("self.h_"+quant+"[0].Write()")
