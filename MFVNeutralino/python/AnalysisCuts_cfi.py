import FWCore.ParameterSet.Config as cms

mfvAnalysisCuts = cms.EDFilter('MFVAnalysisCuts',
                               mevent_src = cms.InputTag('mfvEvent'),
                               trigger_bit = cms.int32(0),
                               re_trigger = cms.bool(False),
                               min_4th_jet_pt = cms.double(60),
                               min_5th_jet_pt = cms.double(0),
                               min_6th_jet_pt = cms.double(0),
                               min_njets = cms.int32(4),
                               max_njets = cms.int32(100000),
                               min_nbtags = cms.vint32(0,0,0),
                               max_nbtags = cms.vint32(100000,100000,100000),
                               min_sum_ht = cms.double(0),
                               min_nsemilepmuons = cms.int32(0),
                               min_nleptons = cms.int32(0),
                               vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                               min_nvertex = cms.int32(2),
                               min_ntracks01 = cms.int32(15),
                               min_maxtrackpt01 = cms.double(15),
                               min_njetssharetks01 = cms.int32(0),
                               min_mass01 = cms.double(0),
                               min_jetsmassntks01 = cms.double(0),
                               )
