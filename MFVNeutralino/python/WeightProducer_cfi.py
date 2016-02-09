import FWCore.ParameterSet.Config as cms

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           mevent_src = cms.InputTag('mfvEvent'),
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           weight_gen = cms.bool(False),
                           weight_gen_sign_only = cms.bool(False),
                           weight_pileup = cms.bool(True),
                           pileup_weights = cms.vdouble(0.4430900689834877, 0.7774946230174374, 1.211532146615326, 1.5555095481485082, 1.3656299694579321, 1.9513380206283242, 1.4311409855780286, 1.2555573073998676, 1.3509572272968273, 1.3430021765269047, 1.2671533450149761, 1.1830775671347276, 1.0767805180896135, 0.9110431461207203, 0.6971726104245397, 0.48543658081115554, 0.32209366814732293, 0.22848641867558733, 0.19027360131827362, 0.15527725489164057, 0.09487219082044276, 0.04095796584834362, 0.013672759117602781, 0.003987335129679708, 0.0011389782126837726, 0.00033784224878244623, 0.00010191256127555789, 2.9928259966798484e-05, 8.357594204838038e-06, 2.2051905560049044e-06, 5.493198439639333e-07, 1.2915574040259908e-07, 2.8638852677561204e-08, 5.978815170388724e-09, 1.1718664799704302e-09, 2.147556635829967e-10, 3.658973660525496e-11, 5.759196292572524e-12, 8.200005561089732e-13, 1.0437472148786202e-13),
                           )
