# JETMET_task


## Setup the framework

```
hltGetConfiguration /online/collisions/2018/2e34/v3.6/HLT/V4 --path HLTriggerFirstPath,HLT_PFMET120_PFMHT120_IDTight_v20,HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned_v9,HLTriggerFinalPath,HLTAnalyzerEndpath --input root://cms-xrd-global.cern.ch//store/data/Run2018C/SingleMuon/RAW/v1/000/320/065/00000/FA37880C-078E-E811-BF6E-02163E015C96.root --full --offline --data --prescale none --output none --process TEST --globaltag 101X_dataRun2_HLT_v7 --setup /dev/CMSSW_10_1_0/GRun > hlt.py
```


## Removing Filter from the path
 removed `process.HLTHBHENoiseCleanerSequence` from the path. Changed input in `process.hltMetClean`
 
 
 ## Making ntuples
 
 Added following line in the `hlt.py` file
 
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
 
