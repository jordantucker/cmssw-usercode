import FWCore.ParameterSet.Config as cms

mfvVertices = cms.EDProducer('MFVVertexer',
                             kvr_params = cms.PSet(
                                 maxDistance = cms.double(0.01),
                                 maxNbrOfIterations = cms.int32(10),
                                 doSmoothing = cms.bool(True),
                                 ),
                             avr_params = cms.PSet(
                                 finder = cms.string('avr'),
                                 primcut = cms.double(1.0),
                                 seccut = cms.double(3),
                                 smoothing = cms.bool(True)
                                 ),
                             beamspot_src = cms.InputTag('offlineBeamSpot'),
                             primary_vertices_src = cms.InputTag('offlinePrimaryVertices'),
                             use_tracks = cms.bool(True),
                             track_src = cms.InputTag('generalTracks'),
                             use_pf_candidates = cms.bool(False),
                             pf_candidate_src = cms.InputTag('particleFlow'),
                             use_pf_jets = cms.bool(False),
                             pf_jet_src = cms.InputTag('ak5PFJets'),
                             use_pat_jets = cms.bool(False),
                             pat_jet_src = cms.InputTag('selectedPatJetsPF'),
                             min_seed_jet_pt = cms.double(30),
                             min_all_track_pt = cms.double(1),
                             min_all_track_dxy = cms.double(0.01),
                             min_all_track_nhits = cms.int32(8),
                             min_all_track_npxhits = cms.int32(0),
                             max_all_track_dxyerr = cms.double(-1),
                             max_all_track_d3derr = cms.double(-1),
                             min_seed_track_pt = cms.double(1),
                             min_seed_track_dxy = cms.double(0.01),
                             min_seed_track_nhits = cms.int32(8),
                             min_seed_track_npxhits = cms.int32(0),
                             max_seed_track_dxyerr = cms.double(-1),
                             max_seed_track_d3derr = cms.double(-1),
                             seed_by_sums = cms.bool(False),
                             min_seed_sum_pt = cms.double(2),
                             min_seed_sum_dxy = cms.double(0),
                             min_seed_sum_adxy = cms.double(0.02),
                             min_seed_sum_nhits = cms.int32(16),
                             max_seed_vertex_chi2 = cms.double(5),
                             use_2d_vertex_dist = cms.bool(False),
                             use_2d_track_dist = cms.bool(False),
                             merge_anyway_dist = cms.double(-1),
                             merge_anyway_sig = cms.double(3),
                             merge_shared_dist = cms.double(-1),
                             merge_shared_sig = cms.double(4),
                             max_track_vertex_dist = cms.double(-1),
                             max_track_vertex_sig = cms.double(5),
                             min_track_vertex_sig_to_remove = cms.double(1.5),
                             remove_one_track_at_a_time = cms.bool(True),
                             histos = cms.untracked.bool(False),
                             verbose = cms.untracked.bool(False),
                             )
