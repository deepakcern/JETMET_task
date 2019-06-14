name = 'HLT_JetMET_ntuple'

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
    
config.General.workArea = 'crab_'+name
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'EGamama'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'hlt_path_withFilter.py'
#config.JobType.maxMemoryMB = 2400
config.JobType.numCores = 4
config.JobType.outputFiles = ['hltJetMetNtuple.root']

config.Data.inputDBS = 'global'
config.Data.splitting ='FileBased'# 'EventAwareLumiBased'
#config.Data.publication = False
#config.Data.lumiMask = '/afs/cern.ch/user/m/mdjordje/public/2018JSON/Cert_322407-323775_13TeV_PromptReco_Collisions18_JSON.txt'
config.Data.publication = False 
   
config.Data.inputDataset = '/EGamma/Run2018C-v1/RAW'
config.Data.unitsPerJob =100# 10000#1000
#config.Data.totalUnits = 1000000
config.Data.outputDatasetTag = 'EGamma'
config.Site.storageSite = 'T2_IN_TIFR'
config.Data.outLFNDirBase = '/store/user/%s/t3store2/HLT_JetMET_ntupels_10062019' % (getUsernameFromSiteDB())

