import sys, FWCore.ParameterSet.Config as cms

version = 'v4'
runOnMC = True # Submit script expects this line to be unmodified...

################################################################################

process = cms.Process('PAT')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(25))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/mc/Summer12/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S7_START52_V9-v2/0000/E4964FC2-A9B8-E111-A9D0-003048FFCBFC.root'))
#process.source.fileNames = ['/store/mc/Summer12/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/AODSIM/PU_S7_START52_V9-v1/0000/FEF1895C-15A4-E111-9EC5-003048D3CDE0.root']
#process.source.fileNames = ['/store/user/tucker/mfvneutralino_genfsimreco_tau100um/mfvneutralino_genfsimreco_tau100um//465709e5340ac2cc11e2751b48bbef3e/fastsim_9_1_7gz.root']
#process.source.fileNames = ['/store/data/Run2012A/MuHad/AOD/PromptReco-v1/000/190/645/9220A9CD-8E82-E111-9938-001D09F24EE3.root']
#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('190645:10-190645:11')
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATSummaryTables')
process.MessageLogger.cerr.PATSummaryTables = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.load('Configuration.StandardSequences.Geometry_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START52_V9E::All' if runOnMC else 'GR_P_V39_AN2::All'

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('pat.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               outputCommands = cms.untracked.vstring(*patEventContent),
                               )
process.outp = cms.EndPath(process.out)

process.load('JMTucker.Tools.PATTupleSelection_cfi')

# Event cleaning, with MET cleaning recommendations from
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'
from DPGAnalysis.Skims.goodvertexSkim_cff import noscraping as FilterOutScraping
process.FilterOutScraping = FilterOutScraping
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(True)
process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')
process.load('RecoMET.METAnalyzers.CSCHaloFilter_cfi')
process.load('RecoMET.METFilters.hcalLaserEventFilter_cfi')
process.hcalLaserEventFilter.vetoByRunEventNumber = False
process.hcalLaserEventFilter.vetoByHBHEOccupancy  = True
process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
process.EcalDeadCellTriggerPrimitiveFilter.tpDigiCollection = cms.InputTag('ecalTPSkimNA')
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')
process.trackingFailureFilter.VertexSource = cms.InputTag('goodOfflinePrimaryVertices')
process.load('RecoMET.METFilters.eeBadScFilter_cfi')

# Instead of filtering out events at tupling time, schedule separate
# paths for all the "good data" filters so that the results of them
# get stored in a small TriggerResults::PAT object, which can be
# accessed later. Make one path for each so they can be accessed
# separately in the TriggerResults object; the "All" path that is the
# product of all of the filters isn't necessary but it's nice for
# convenience.
filters = [(name, getattr(process, name)) for name in process.jtupleParams.eventFilters.value()]
process.eventCleaningAll = cms.Path()
for filter, filter_obj in filters:
    setattr(process, 'eventCleaning' + filter, cms.Path(filter_obj))
    process.eventCleaningAll *= filter_obj

################################################################################

# PAT/PF2PAT configuration inspired by TopQuarkAnalysis/Configuration
# (test/patRefSel_allJets_cfg.py and included modules) with tag
# V07-00-01.

# First, turn off stdout so that the spam from PAT/PF2PAT doesn't
# flood the screen (especially useful in batch job submission).
suppress_stdout = True
if suppress_stdout:
    print 'tuple.py: PAT would spam a lot of stuff to stdout... hiding it.'
    from cStringIO import StringIO
    old_stdout = sys.stdout
    sys.stdout = buf = StringIO()

jecLevels = ['L1FastJet', 'L2Relative', 'L3Absolute']
#jecLevels.pop(0); jecLevels.insert(0, 'L1Offset')
if not runOnMC:
    jecLevels.append('L2L3Residual')
#jecLevels += ['L5Flavor', 'L7Parton']

postfix = 'PF'
def processpostfix(name):
    return getattr(process, name + postfix)
def setprocesspostfix(name, obj):
    setattr(process, name + postfix, obj)
def InputTagPostFix(name):
    return cms.InputTag(name + postfix)

process.load('PhysicsTools.PatAlgos.patSequences_cff')
from PhysicsTools.PatAlgos.tools.pfTools import usePF2PAT
usePF2PAT(process,
          runPF2PAT = True,
          runOnMC = runOnMC,
          jetAlgo = 'AK5',
          postfix = postfix,
          jetCorrections = ('AK5PFchs', jecLevels), # 'chs': using PFnoPU
          typeIMetCorrections = True,
          pvCollection = cms.InputTag('goodOfflinePrimaryVertices'),
          )

processpostfix('pfNoPileUp')  .enable = True  # usePFnoPU
processpostfix('pfNoMuon')    .enable = True  # useNoMuon
processpostfix('pfNoElectron').enable = True  # useNoElectron
processpostfix('pfNoJet')     .enable = True  # useNoJet
processpostfix('pfNoTau')     .enable = True  # useNoTau

if 'L1FastJet' in jecLevels:
    processpostfix('pfPileUpIso').checkClosestZVertex = True # usePfIsoLessCHS: switch to new PF isolation with L1Fastjet CHS

processpostfix('pfMuonsFromVertex').d0Cut = processpostfix('pfElectronsFromVertex').d0Cut = 0.2
processpostfix('pfMuonsFromVertex').dzCut = processpostfix('pfElectronsFromVertex').dzCut = 0.5

processpostfix('pfSelectedMuons').cut = 'pt > 5.'
#processpostfix('pfSelectedMuons').cut += process.jtupleParams.muonCut
processpostfix('pfIsolatedMuons').isolationCut = 0.2

if False: # pfMuonIsoConeR03
    processpostfix('pfIsolatedMuons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('muPFIsoValueCharged03'))
    processpostfix('pfIsolatedMuons').deltaBetaIsolationValueMap = InputTagPostFix('muPFIsoValuePU03')
    processpostfix('pfIsolatedMuons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('muPFIsoValueNeutral03'), InputTagPostFix('muPFIsoValueGamma03'))
    processpostfix('pfMuons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('muPFIsoValueCharged03'))
    processpostfix('pfMuons').deltaBetaIsolationValueMap = InputTagPostFix('muPFIsoValuePU03')
    processpostfix('pfMuons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('muPFIsoValueNeutral03'), InputTagPostFix('muPFIsoValueGamma03'))
    processpostfix('patMuons').isolationValues.pfNeutralHadrons   = InputTagPostFix('muPFIsoValueNeutral03')
    processpostfix('patMuons').isolationValues.pfChargedAll       = InputTagPostFix('muPFIsoValueChargedAll03')
    processpostfix('patMuons').isolationValues.pfPUChargedHadrons = InputTagPostFix('muPFIsoValuePU03')
    processpostfix('patMuons').isolationValues.pfPhotons          = InputTagPostFix('muPFIsoValueGamma03')
    processpostfix('patMuons').isolationValues.pfChargedHadrons   = InputTagPostFix('muPFIsoValueCharged03')

processpostfix('pfSelectedElectrons').cut = 'pt > 5. && gsfTrackRef.isNonnull && gsfTrackRef.trackerExpectedHitsInner.numberOfLostHits < 2'
#processpostfix('pfSelectedElectrons').cut += ' && ' + process.jtupleParams.electronCut # disabled by default, but can use minimal (veto) electron selection cut on top of pfElectronSelectionCut
processpostfix('pfIsolatedElectrons').isolationCut = 0.2

if True: # pfElectronIsoConeR03
    processpostfix('pfIsolatedElectrons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('elPFIsoValueCharged03PFId'))
    processpostfix('pfIsolatedElectrons').deltaBetaIsolationValueMap = InputTagPostFix('elPFIsoValuePU03PFId')
    processpostfix('pfIsolatedElectrons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('elPFIsoValueNeutral03PFId'), InputTagPostFix('elPFIsoValueGamma03PFId'))
    processpostfix('pfElectrons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('elPFIsoValueCharged03PFId'))
    processpostfix('pfElectrons').deltaBetaIsolationValueMap = InputTagPostFix('elPFIsoValuePU03PFId')
    processpostfix('pfElectrons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('elPFIsoValueNeutral03PFId'), InputTagPostFix('elPFIsoValueGamma03PFId'))
    processpostfix('patElectrons').isolationValues.pfNeutralHadrons   = InputTagPostFix('elPFIsoValueNeutral03PFId')
    processpostfix('patElectrons').isolationValues.pfChargedAll       = InputTagPostFix('elPFIsoValueChargedAll03PFId')
    processpostfix('patElectrons').isolationValues.pfPUChargedHadrons = InputTagPostFix('elPFIsoValuePU03PFId')
    processpostfix('patElectrons').isolationValues.pfPhotons          = InputTagPostFix('elPFIsoValueGamma03PFId')
    processpostfix('patElectrons').isolationValues.pfChargedHadrons   = InputTagPostFix('elPFIsoValueCharged03PFId')

process.load('EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi')
process.eidMVASequence = cms.Sequence(process.mvaTrigV0 + process.mvaNonTrigV0)
processpostfix('patElectrons').electronIDSources.mvaTrigV0    = cms.InputTag("mvaTrigV0")
processpostfix('patElectrons').electronIDSources.mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0")
processpostfix('patMuons').embedTrack = True
processpostfix('selectedPatElectrons').cut = process.jtupleParams.electronCut
processpostfix('selectedPatMuons').cut = process.jtupleParams.muonCut
processpostfix('selectedPatJets').cut = process.jtupleParams.jetCut
processpostfix('patJets').addTagInfos = True

from PhysicsTools.PatAlgos.tools.coreTools import runOnData, removeSpecificPATObjects
if not runOnMC:
    runOnData(process, names = ['All'], postfix = postfix)
removeSpecificPATObjects(process, names = ['Photons'], postfix = postfix) # will also remove cleaning

# Make some extra SV producers for MFV studies. JMTBAD postfix junk
for cut in (1., 1.5, 2., 2.5, 3.):
    cut_name = ('%.1f' % cut).replace('.', 'p')
                 
    tag_info_name = 'secondaryVertexMaxDR%sTagInfosAODPF' % cut_name
    tag_info_obj = process.secondaryVertexTagInfosAODPF.clone()
    tag_info_obj.vertexCuts.maxDeltaRToJetAxis = cut
    setattr(process, tag_info_name, tag_info_obj)
    process.patJetsPF.tagInfoSources.append(cms.InputTag(tag_info_name))
  
    disc_names = ('simpleSecondaryVertexHighEffBJetTagsAODPF',
                  'simpleSecondaryVertexHighPurBJetTagsAODPF',
                  'combinedSecondaryVertexBJetTagsAODPF',
                  'combinedSecondaryVertexMVABJetTagsAODPF')
    disc_objs = []
    for disc_name in disc_names:
        new_disc_name = disc_name.replace('JetTagsAODPF', 'MaxDR%sJetTagsAODPF' % cut_name)
        if 'simple' in disc_name:
            tags = cms.VInputTag(cms.InputTag(tag_info_name))
        else:
            tags = cms.VInputTag(cms.InputTag("impactParameterTagInfosAODPF"), cms.InputTag(tag_info_name))
        o = getattr(process, disc_name).clone(tagInfos = tags)
        disc_objs.append(o)
        setattr(process, new_disc_name, o)
        process.patJetsPF.discriminatorSources.append(cms.InputTag(new_disc_name))
  
    processpostfix('patPF2PATSequence').replace(processpostfix('patJets'), tag_info_obj * reduce(lambda x,y: x*y, disc_objs) * processpostfix('patJets'))

setprocesspostfix('semilepMuons',     cms.EDFilter('PATMuonSelector',     src = InputTagPostFix('selectedPatMuons'),     cut = process.jtupleParams.semilepMuonCut))
setprocesspostfix('dilepMuons',       cms.EDFilter('PATMuonSelector',     src = InputTagPostFix('selectedPatMuons'),     cut = process.jtupleParams.dilepMuonCut))
setprocesspostfix('semilepElectrons', cms.EDFilter('PATElectronSelector', src = InputTagPostFix('selectedPatElectrons'), cut = process.jtupleParams.semilepElectronCut))
setprocesspostfix('dilepElectrons',   cms.EDFilter('PATElectronSelector', src = InputTagPostFix('selectedPatElectrons'), cut = process.jtupleParams.dilepElectronCut))

setprocesspostfix('countPatLeptonsSemileptonic', processpostfix('countPatLeptons').clone(minNumber = 1, muonSource = InputTagPostFix('semilepMuons'), electronSource = InputTagPostFix('semilepElectrons')))
setprocesspostfix('countPatLeptonsDileptonic',   processpostfix('countPatLeptons').clone(minNumber = 2, muonSource = InputTagPostFix('dilepMuons'),   electronSource = InputTagPostFix('dilepElectrons')))

# Require numbers of jets based on the trigger: hadronic channel will
# have at least a 4-jet trigger (maybe 6!), while semileptonic uses a
# 3-jet trigger. Dileptonic has no jets in trigger, but we'll require
# at least one b-tag anyway.
setprocesspostfix('countPatJetsHadronic',     processpostfix('countPatJets').clone(minNumber = 4))
setprocesspostfix('countPatJetsSemileptonic', processpostfix('countPatJets').clone(minNumber = 3))
setprocesspostfix('countPatJetsDileptonic',   processpostfix('countPatJets').clone(minNumber = 1))

channels = ('Hadronic', 'Semileptonic', 'Dileptonic')
obj = cms.ignore(process.goodOfflinePrimaryVertices) + cms.ignore(process.mvaTrigV0) + cms.ignore(process.mvaNonTrigV0) + processpostfix('patPF2PATSequence')
for channel in channels:
    setattr(process, 'p' + channel, cms.Path(obj))

process.pHadronic     *= processpostfix('countPatJetsHadronic')
process.pSemileptonic *= processpostfix('countPatJetsSemileptonic') + processpostfix('semilepMuons') + processpostfix('semilepElectrons') + processpostfix('countPatLeptonsSemileptonic')
process.pDileptonic   *= processpostfix('countPatJetsDileptonic')   + processpostfix('dilepMuons')   + processpostfix('dilepElectrons')   + processpostfix('countPatLeptonsDileptonic')

process.out.SelectEvents.SelectEvents = ['p' + channel for channel in channels]
process.out.outputCommands = [
    'drop *',
    'keep *_selectedPatElectrons*_*_*',
    'keep *_selectedPatMuons*_*_*',
    'keep *_semilep*_*_*',
    'keep *_dilep*_*_*',
    'keep *_selectedPatJets*_*_*',
    'keep *_selectedPatJets*_genJets_*',
    'drop *_selectedPatJets*_pfCandidates_*',
    'drop *_selectedPatJetsForMETtype1p2CorrPF_*_*',
    'drop *_selectedPatJetsForMETtype2CorrPF_*_*',
    'drop CaloTowers_*_*_*',
    'keep *_patMETs*_*_*',
    'keep recoGenParticles_genParticles_*_*',
    'keep GenEventInfoProduct_*_*_*',
    'keep GenRunInfoProduct_*_*_*',
    'keep PileupSummaryInfos_addPileupInfo__*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_goodOfflinePrimaryVertices_*_*',
    'keep edmTriggerResults_TriggerResults__HLT*',
    'keep edmTriggerResults_TriggerResults__REDIGI*',
    'keep edmTriggerResults_TriggerResults__PAT', # for post-tuple filtering on the goodData paths
    'keep *_hltTriggerSummaryAOD__HLT*',
    'keep *_hltTriggerSummaryAOD__REDIGI*',
    ]

# The normal TrigReport doesn't state how many events are written
# total to the file in case of OutputModule's SelectEvents having
# multiple paths. Add a summary to stdout that so that it is easy to
# see what the total number of events should be (for debugging CRAB
# jobs).
process.ORTrigReport = cms.EDAnalyzer('ORTrigReport',
                                      results_src = cms.InputTag('TriggerResults', '', process.name_()),
                                      paths = process.out.SelectEvents.SelectEvents
                                      )
process.pORTrigReport = cms.EndPath(process.ORTrigReport) # Must be on an EndPath.

# Check that the stdout spam from PAT was what we expect.
if suppress_stdout:
    pat_output = buf.getvalue()
    sys.stdout = old_stdout
    buf.close()
    hsh = hash(pat_output)
    #open('pat_spam.txt', 'wt').write(pat_output)
    hsh_expected = 4533816878313021228 if runOnMC else -3882518544097161276
    print 'PAT is done (spam hash %s, expected %s).' % (hsh, hsh_expected)
    if hsh != hsh_expected:
        from JMTucker.Tools.general import big_warn
        big_warn('Unexpected spam hash! Did you change an option?')

def input_is_fastsim():
    for name in 'HBHENoiseFilter CSCTightHaloFilter'.split():
        delattr(process, 'eventCleaning' + name)
        process.eventCleaningAll.remove(getattr(process, name))
    process.pfNoPileUp.bottomCollection = 'FSparticleFlow'
    process.pfPileUp.PFCandidates = 'FSparticleFlow'
    process.pfCandsNotInJetPF.bottomCollection = 'FSparticleFlow'

def input_is_pythia8():
    process.patJetPartonMatch.mcStatus = cms.vint32(21,22,23,24,25,26,27,28,29)
    process.patJetPartonMatchPF.mcStatus = cms.vint32(21,22,23,24,25,26,27,28,29)

def keep_general_tracks():
    process.out.outputCommands.append('keep *_generalTracks_*_*')

#input_is_fastsim()
#input_is_pythia8()
#keep_general_tracks()

#open('dumptup.py','wt').write(process.dumpPython())

