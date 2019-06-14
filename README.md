# JETMET_task


## Setup the framework
```
cmsrel CMSSW_10_1_11_patch1
cd CMSSW_10_1_11_patch1/src
cmsenv
git cms-addpkg HLTrigger/Configuration

# Dependencies and Compilation
git cms-checkdeps -A -a
scram b -j 8
cd HLTrigger/Configuration/test
```

```
hltGetConfiguration /online/collisions/2018/2e34/v3.6/HLT/V4 --path HLTriggerFirstPath,HLT_PFMET120_PFMHT120_IDTight_v20,HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned_v9,HLTriggerFinalPath,HLTAnalyzerEndpath --input root://cms-xrd-global.cern.ch//store/data/Run2018C/SingleMuon/RAW/v1/000/320/065/00000/FA37880C-078E-E811-BF6E-02163E015C96.root --full --offline --data --prescale none --output none --process TEST --globaltag 101X_dataRun2_HLT_v7 --setup /dev/CMSSW_10_1_0/GRun > hlt_path_withFilter.py
```


## Removing Filter from the path
 removed `process.HLTHBHENoiseCleanerSequence` from the path [HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned_v9, HLT_PFMET120_PFMHT120_IDTight_v20]. Changed input in `process.hltMetClean`
 
 
 ## Adding EDAnalyser in the framework
 
 ```
cd HLTrigger/Configuration
mkdir plugins
 ```
 
 Copy `hltAnalyzer.cc` and `Build.xml` files inside the `plugins` directory.
 Copy `hltJetMETNtuple_new_cfi.py` file inside `python` directory.
 And compile files agian.
 ```
 cd src/
 scram b -j 8
 ```
 
 ## Making ntuples
 
 Added following line in the `hlt_path_withFilter.py` file
 
 ```
 from HLTrigger.Configuration.hltJetMETNtuple_new_cfi import *
configureJetMetNtuple(process)
process.ntuple = cms.EndPath(process.hltJetMetNtuple)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("hltJetMetNtuple.root")
 ```
 
 ## Submitting Crab jobs
 
 ```
 crab submit -c crab.py
 ```
 
 ## Plotting Trigger Efficiency
 ```
 python TriggerEfficiency.py -i inputNtuplesfiles.txt -D .
 python EfficiencyPlotter.py 
 ```
 
