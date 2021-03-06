// -*- C++ -*-
//
// Package:    Demo/DemoAnalyzer
// Class:      DemoAnalyzer
// 
/**\class DemoAnalyzer DemoAnalyzer.cc Demo/DemoAnalyzer/plugins/DemoAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Deepak Kumar
//         Created:  Wed, 10 Apr 2019 11:55:44 GMT
//
//


// system include files
#include <memory>
#include <string>
#include <iostream>
#include <vector>
#include "TTree.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "Math/VectorUtil.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"

#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Common/interface/TriggerNames.h"


//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class hltAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
   public:
      explicit hltAnalyzer(const edm::ParameterSet&);
      ~hltAnalyzer();
      //void SetBranches();
    //  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
      


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      TTree* tree_;
      //edm::EDGetTokenT<View<pat::Jet> > jetToken_;
      edm::EDGetTokenT<reco::PFMETCollection> pfMETRawToken_;
      edm::EDGetTokenT<reco::MuonCollection> hltmuonToken_;
      //edm::Handle< edm::View<reco::MET> > pfMETRawToken_;
      edm::EDGetTokenT<reco::CaloMETCollection> caloMETRawToken_;
 //     edm::EDGetTokenT<reco::MuonCollection> hltmuonToken_;
      //edm::Handle< edm::View<reco::MET> > pfMETRawToken_;
      edm::EDGetTokenT<edm::TriggerResults>   trigResultsToken;
      //void SetBranches();
      unsigned long run_,event_,lumi_;
      float CaloMET;
      float pfrawMET;
      std::vector<bool> trigResult_;
      std::vector<float> muonPx_;
      std::vector<float> muonPy_;
      std::vector<float> muonPz_;
      std::vector<float> muonE_;
      std::vector<std::string> trigName_;
      int nTrigs_;
      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//
//
// constructors and destructor
//
hltAnalyzer::hltAnalyzer(const edm::ParameterSet& iConfig):
//jetToken_( consumes<View<pat::Jet> >( iConfig.getParameter<InputTag> ( "JetTag" ) ) )
pfMETRawToken_(consumes<reco::PFMETCollection>(iConfig.getParameter<edm::InputTag>("pfMetRaw"))),
hltmuonToken_(consumes<reco::MuonCollection>(iConfig.getParameter<edm::InputTag>("MuonCollectionTag"))),
caloMETRawToken_(consumes<reco::CaloMETCollection> (iConfig.getParameter<edm::InputTag>("caloMetRaw"))),
trigResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerLabel")))
//jetToken_( iConfig.getParameter<InputTag> ( "JetTag" ) )
{
usesResource("TFileService");
//edm::Service<TFileService> fs;
//tree_ = fs->make<TTree>("tree_","tree");
//produces<vector<pat::Jet> >(); 
  //now do what ever initialization is needed
   //usesResource("TFileService");
//jetToken_( consumes<View<pat::Jet> >( iConfig.getParameter<InputTag> ( "JetTag" ) ) )

}


hltAnalyzer::~hltAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
hltAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
//  Clear();
   using namespace edm;
   using namespace std;


 // event info
  run_   = iEvent.id().run();
  event_ = iEvent.id().event();
  lumi_  = iEvent.getLuminosityBlock().luminosityBlock();


 Handle<reco::PFMETCollection> pfMetRawHandle;
 Handle<reco::CaloMETCollection> caloMetRawHandle;

 Handle<edm::TriggerResults> trigResults;

 Handle<reco::MuonCollection> muons;

// Handle<View<pat::Jet> > jets;
 //iEvent.getByToken( jetToken_, jets );
 if (not iEvent.getByToken(caloMETRawToken_,caloMetRawHandle)){
	std::cout << ">>> CaloMET collection does not exist !!!\n";
	return;
	}


 if (not iEvent.getByToken(pfMETRawToken_,pfMetRawHandle)){
        std::cout << ">>> pfMET collection does not exist !!!\n";
        return;}


 if (not iEvent.getByToken(trigResultsToken, trigResults)){
 std::cout << ">>> TRIGGER collection does not exist !!!\n";
 return;
 }

 if (not iEvent.getByToken(hltmuonToken_, muons)){
 std::cout << ">>> Muon collection does not exist !!!\n";
 return;
 }



 CaloMET= -9999;
 pfrawMET=-9999;



 auto calometraw=caloMetRawHandle.product()->begin();
 CaloMET = calometraw->et();
 std::cout << " calo raw met " << calometraw->et() << std::endl;

 auto pfmetraw=pfMetRawHandle.product()->begin();
 pfrawMET = pfmetraw->et();

 //std::cout << " pfmetraw->et() : " << pfmetraw->et() << " pfmetraw->pt() " << pfmetraw->pt() << std::endl;
 std::cout << " raw met " << pfmetraw->et() << std::endl;

 const edm::TriggerNames & trigNames = iEvent.triggerNames(*trigResults);

 reco::MuonCollection muColl(*(muons.product()));


 trigName_.clear();
 trigResult_.clear();
 muonPx_.clear();
 muonPy_.clear();
 muonPz_.clear();
 muonE_.clear();




 reco::MuonCollection::const_iterator mu;
 for(mu=muColl.begin(); mu!=muColl.end(); mu++){
 if(mu->pt() < 10.) continue;
 if(TMath::Abs(mu->eta()) > 2.5) continue;
 if (not mu->isGlobalMuon()) continue;
 muonPx_.push_back(mu->p4().px());
 muonPy_.push_back(mu->p4().py());
 muonPz_.push_back(mu->p4().pz());
// muonPt_.push_back(mu->pt());
 muonE_.push_back(mu->energy());
 //std::cout << "muon testing" << std::endl;
}


 for (unsigned int i=0; i<trigResults->size(); i++){
 std::string trigName = trigNames.triggerName(i);

 if(0){std::cout << "trigName" << trigName << std::endl;};

 bool trigResult = trigResults->accept(i);
 if(0){std::cout << " trigResult " << trigResult << std::endl;};






 trigName_.push_back(trigName);
 trigResult_.push_back(trigResult);

 }


tree_->Fill();

/*
for(auto j = jets->begin(); j != jets->end(); ++j){
        if(j->pt() < 150.) continue;
        std::cout << "jetpT : " << j->pt() << std::endl;
        std::cout << "deepDoubleB = " << j->bDiscriminator("pfMassIndependentDeepDoubleBvLJetTags:probHbb") << std::endl;
}*/

//#ifdef THIS_IS_AN_EVENT_EXAMPLE
   //Handle<ExampleData> pIn;
   //iEvent.getByLabel("example",pIn);
//#endif
   
//#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   //ESHandle<SetupData> pSetup;
   //iSetup.get<SetupRecord>().get(pSetup);
//#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
hltAnalyzer::beginJob()
{
	edm::Service<TFileService> fs;
	tree_ = fs->make<TTree>("tree_","tree");

	tree_->Branch("run", &run_, "run/l");
	tree_->Branch("event", &event_, "event/l");
	tree_->Branch("lumi", &lumi_, "lumi/l");

	tree_->Branch("CaloMET",&CaloMET, "CaloMET/f");
	tree_->Branch("pfrawMET",&pfrawMET,"pfrawMET/f");
	//tree_->Branch("trigResult",&trigResult_, "trigResult/O");
	//	//tree_->Branch("trigName",&trigName_, "trigName/C");
	tree_->Branch("trigResult", "std::vector<bool>", &trigResult_);
	tree_->Branch("trigName", "std::vector<std::string>", &trigName_);
        tree_->Branch("muonPx","std::vector<float>",&muonPx_);
        tree_->Branch("muonPy","std::vector<float>",&muonPy_);
        tree_->Branch("muonPz","std::vector<float>",&muonPz_);
        tree_->Branch("muonE","std::vector<float>",&muonE_);

        //float dummy = -99999;
        //trigName_.clear();
        //trigResult_.clear();
        //CaloMET=dummy;

}

// ------------ method called once each job just after ending the event loop  ------------
void 
hltAnalyzer::endJob() 
{/*
	float dummy = -99999;
	trigName_.clear();
	trigResult_.clear();
	CaloMET=dummy;
*/
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------

//define this as a plug-in
DEFINE_FWK_MODULE(hltAnalyzer);
