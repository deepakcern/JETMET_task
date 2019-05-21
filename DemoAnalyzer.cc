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

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

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

class DemoAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
   public:
      explicit DemoAnalyzer(const edm::ParameterSet&);
      ~DemoAnalyzer();
      //void SetBranches();
    //  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
      


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      TTree* tree_;
      //edm::EDGetTokenT<View<pat::Jet> > jetToken_;
      edm::EDGetTokenT<reco::PFMETCollection> pfMETRawToken_;
      //edm::Handle< edm::View<reco::MET> > pfMETRawToken_;
      edm::EDGetTokenT<reco::CaloMETCollection> caloMETRawToken_;
      //edm::Handle< edm::View<reco::MET> > pfMETRawToken_;
      edm::EDGetTokenT<edm::TriggerResults>   trigResultsToken;
      //void SetBranches();
      float CaloMET;
      float pfrawMET;
      std::vector<bool> trigResult_;
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
DemoAnalyzer::DemoAnalyzer(const edm::ParameterSet& iConfig):
//jetToken_( consumes<View<pat::Jet> >( iConfig.getParameter<InputTag> ( "JetTag" ) ) )
pfMETRawToken_(consumes<reco::PFMETCollection>(iConfig.getParameter<edm::InputTag>("pfMetRaw"))),
//caloMETRawToken_(consumes<reco::CaloMETCollection> (iConfig.getParameter<edm::InputTag>("caloMetRaw"))),
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


DemoAnalyzer::~DemoAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
DemoAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
//  Clear();
   using namespace edm;
   using namespace std;


 Handle<reco::PFMETCollection> pfMetRawHandle;
 //Handle<reco::CaloMETCollection> caloMetRawHandle;



 Handle<edm::TriggerResults> trigResults;

// Handle<View<pat::Jet> > jets;
 //iEvent.getByToken( jetToken_, jets );
 //if (not iEvent.getByToken(caloMETRawToken_,caloMetRawHandle)){
//	std::cout << ">>> CaloMET collection does not exist !!!\n";
//	return;
//	}


 if (not iEvent.getByToken(pfMETRawToken_,pfMetRawHandle)){
        std::cout << ">>> pfMET collection does not exist !!!\n";
        return;
        }


 if (not iEvent.getByToken(trigResultsToken, trigResults)){
 std::cout << ">>> TRIGGER collection does not exist !!!\n";
 return;
 }


 CaloMET= -9999;
 pfrawMET=-9999;
 //auto calometraw=caloMetRawHandle.product()->begin();
 //CaloMET = calometraw->sumEt();
 //std::cout << " raw met " << calometraw->sumEt() << std::endl;

 auto pfmetraw=pfMetRawHandle.product()->begin();
 pfrawMET = pfmetraw->sumEt();
 //std::cout << " raw met " << pfmetraw->sumEt() << std::endl;

 const edm::TriggerNames & trigNames = iEvent.triggerNames(*trigResults);


 trigName_.clear();
 trigResult_.clear();
 for (unsigned int i=0; i<trigResults->size(); i++){


 std::string trigName = trigNames.triggerName(i);

 if(1){std::cout << "trigName" << trigName << std::endl;};

 bool trigResult = trigResults->accept(i);
 if(1){std::cout << " trigResult " << trigResult << std::endl;};

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
DemoAnalyzer::beginJob()
{
	edm::Service<TFileService> fs;
	tree_ = fs->make<TTree>("tree_","tree");
	//tree_->Branch("run", &run_, "run/l");
	//tree_->Branch("event", &event_, "event/l");	
//	tree_->Branch("CaloMET",&CaloMET, "CaloMET/f");
	tree_->Branch("pfrawMET",&pfrawMET,"pfrawMET/f");
	//tree_->Branch("trigResult",&trigResult_, "trigResult/O");
	//	//tree_->Branch("trigName",&trigName_, "trigName/C");
	tree_->Branch("trigResult", "std::vector<bool>", &trigResult_);
	tree_->Branch("trigName", "std::vector<std::string>", &trigName_);

        //float dummy = -99999;
        //trigName_.clear();
        //trigResult_.clear();
        //CaloMET=dummy;

}

// ------------ method called once each job just after ending the event loop  ------------
void 
DemoAnalyzer::endJob() 
{/*
	float dummy = -99999;
	trigName_.clear();
	trigResult_.clear();
	CaloMET=dummy;
*/
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------

//define this as a plug-in
DEFINE_FWK_MODULE(DemoAnalyzer);
