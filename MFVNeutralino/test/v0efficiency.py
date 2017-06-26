from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.MFVNeutralino.Year import year

is_mc = False
H = False

process = pat_tuple_process(None, is_mc, year, H)
jets_only(process)
tfileservice(process, 'v0efficiency.root')

process.source.fileNames = ['/store/data/Run2016E/ZeroBias/AOD/23Sep2016-v1/100000/18151C77-4486-E611-84FD-0CC47A7C357A.root']

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(True)

process.v0eff = cms.EDAnalyzer('MFVV0Efficiency',
                               kvr_params = cms.PSet(maxDistance = cms.double(0.01),
                                                     maxNbrOfIterations = cms.int32(10),
                                                     doSmoothing = cms.bool(True),
                                                     ),
                               pileup_weights = cms.vdouble(*pileup_weights[year]),
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                               tracks_src = cms.InputTag('generalTracks'),
                               #debug = cms.untracked.bool(True)
                               )

process.p = cms.Path(process.goodOfflinePrimaryVertices * process.v0eff)

process.maxEvents.input = -1
set_lumis_to_process_from_json(process, 'ana_2016.json')
#report_every(process, 1)
#want_summary(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    samples = Samples.data_samples + [s for s in Samples.auxiliary_data_samples if s.name.startswith('ZeroBias')]
    for s in samples:
        s.files_per = 50

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('V0EfficiencyV1')
    ms.common.ex = year
    ms.common.pset_modifier = H_modifier #chain_modifiers(is_mc_modifier, H_modifier)
    ms.crab.job_control_from_sample = True
    ms.submit(samples)