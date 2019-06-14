from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend,gROOT
from ROOT import kBlack, kBlue, kRed
from array import array


f = TFile.Open('Output_HLT_JetMET_ntupels.root')
f2 = TFile.Open('Output_HLT_JetMET_ntupels_NoF.root')


#f = TFile.Open('Output_HLT_JetMET_ntupels.root')
#f2 = TFile.Open('Output_Full_withoutFilter1_ntuples.root')
gStyle.SetErrorX(0.5)
# gStyle.SetFrameLineWidth(3)
# gStyle.SetOptTitle(0)
# gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0)
# gStyle.SetFillColor(2)
# gStyle.SetLineWidth(1)
# gStyle.SetHistFillStyle(2)
gROOT.SetBatch(1)
#bins=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,160,170,180,190,200,220,240,260,280,300,350,400,500,600,700,800,1000,1200,1500,2000]
bins=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,160,170,180,190,200,220,240,260,280,300,350,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000]
#bins=[500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000]
#bins=[500,550,600,2000]
#bins=[700,700+260,700+260+260,700+260+260+260,700+260+260+260+260,2000]

#bins=[700,700+433,700+433+433,2000]
#bins=[700,2000]
def setHistStyle(h_temp2,bins):

    h_temp=h_temp2.Rebin(10)#len(bins)-1,"h_temp",array('d',bins))
    h_temp.SetLineWidth(1)
    #h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    #h_temp.SetBinContent(len(bins),0.)
    h_temp.GetXaxis().SetRangeUser(100,1000)
    h_temp.SetMarkerColor(kBlack);
    h_temp.SetMarkerStyle(2);
    return h_temp

def AddText(txt):
    texcms = TLatex(-20.0, 50.0, txt)
    texcms.SetNDC()
    texcms.SetTextAlign(12)
    texcms.SetX(0.5)
    texcms.SetY(0.34)
    texcms.SetTextSize(0.02)
    texcms.SetTextSizePixels(32)
    return texcms

def SetCanvas():

    # CMS inputs
    # -------------
    H_ref = 1000;
    W_ref = 1000;
    W = W_ref
    H  = H_ref

    T = 0.08*H_ref
    B = 0.21*H_ref
    L = 0.12*W_ref
    R = 0.08*W_ref
    # --------------

    c1 = TCanvas("c2","c2",0,0,2000,1500)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetGridy()
    c1.SetGridx()
    #c1.SetLogy(1)
    return c1


def getLegend():
    legend=TLegend(.10,.79,.47,.89)
    legend.SetTextSize(0.038)
    legend.SetFillStyle(0)

    return legend

def getLatex():
    latex =  TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    latex.SetTextAlign(11);
    return latex


def ratioplot():
     # create required parts
     leg=getLegend()
     latex=getLatex()
     c=SetCanvas()
     #c.SetLogy()
     #c = TCanvas()
     #c.SetLogy()

     h1=f.Get('h_num_calo_')#'calo',pf
     h1=setHistStyle(h1,bins)
     h2=f.Get('h_den_calo_')
     h2=setHistStyle(h2,bins)


     h11=f2.Get('h_num_calo_')
     h11=setHistStyle(h11,bins)
     h21=f2.Get('h_den_calo_')
     h21=setHistStyle(h21,bins)

     gr =TGraphAsymmErrors(30)
     #gr.Divide(h1,h2)
     gr=TGraphAsymmErrors(h1,h2)
     gr2=TGraphAsymmErrors(h11,h21)
     gr2.SetMarkerStyle(20)
     gr2.GetXaxis().SetRangeUser(0,1000)
     gr2.SetMarkerSize(1.5)
     gr2.SetLineColor(2)
     gr2.SetLineWidth(1)
     gr2.SetMarkerColor(2)

     gr.GetXaxis().SetRangeUser(0,1000)
    # gr.GetYaxis().SetRangeUser(0.0001,1.2)
     gr.SetMarkerStyle(20)
     gr.SetMarkerSize(1.5)
     gr.SetLineColor(1)
     gr.SetLineWidth(1)
     gr.SetMarkerColor(1)
     gr.GetYaxis().SetTitle("Trigger Efficiency")
     gr.GetXaxis().SetTitle("MET [GeV]")
     gr.SetTitle("")


     #base histogram
     histogram_base = TH1F("histogram_base", "", 1000, 0, 1000.)
     histogram_base.SetTitle("")
     histogram_base.SetStats(0)
     histogram_base.SetMarkerSize(2)
     #histogram_base.SetMinimum(0.0)
     histogram_base.SetMaximum(1.2)
     histogram_base.GetXaxis().SetTitle("Online E_{T}^{miss} (GeV)")
     histogram_base.GetYaxis().SetTitle("Efficiency")
     histogram_base=setHistStyle(histogram_base,bins)


     histogram_base.Draw("HIST")
    # c.SaveAs()

     gr.Draw('P same')
     gr2.Draw('P same')
     latex.DrawLatex(0.49, 0.93, " EGamma Run2018C, 13 TeV")
     xmin=0.0
     line = TLine(max(xmin,gr.GetXaxis().GetXmin()),1,1000,1)
     line.SetLineColor(1)
     line.SetLineWidth(1)
     line.SetLineStyle(7)
     line.Draw()
     leg.AddEntry(gr,'With HBHENoise filter','P')
     leg.AddEntry(gr2,'Without HBHENoise filter','P')
     leg.Draw()

     txt = 'Path: HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned'
     texcms = AddText(txt)
     texcms.Draw("same")

     c.SaveAs('testTurnOn_EGamma.png')


if __name__ == "__main__":
     ratioplot()
