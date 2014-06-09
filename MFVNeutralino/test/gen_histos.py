import os, sys, glob
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

process.source.fileNames = ['/store/user/jchavesb/mfv_ttbar_ali_elliptical/mfv_ttbar_ali_elliptical/84bbc883c4d7ec08aa60419295f8ddab/reco_1000_1_CH2.root']
#process.source.fileNames = ['/store/user/jchavesb/mfv_ttbar_ali_elliptical/mfv_ttbar_ali_elliptical/84bbc883c4d7ec08aa60419295f8ddab/reco_172_1_lj6.root']
#process.source.fileNames = ['/store/user/jchavesb/mfv_neutralino_tau1000um_M0400_tune_3/mfv_neutralino_tau1000um_M0400_tune_3/e17c423e411c7625ebf79112981b92b0/reco_1000_1_5td.root']
process.TFileService.fileName = 'gen_histos2.root'

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.load('JMTucker.MFVNeutralino.GenHistos_cff')
process.mfvGenParticleFilter.cut_invalid = False
process.mfvGenHistos.check_all_gen_particles = False
use_bkg = ('use_bkg' in sys.argv)
process.mfvGenHistos.mci_bkg = use_bkg

if use_bkg:
    process.p = cms.Path(process.mfvGenHistos)
else:
    process.p = cms.Path(process.mfvGenParticleFilter * process.mfvGenHistos)

if debug:
    process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                       src = cms.InputTag('genParticles'),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.p.insert(0, process.printList)
    file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if debug:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    import JMTucker.Tools.Samples as Samples
    #samples = [s for s in Samples.mfv_signal_samples + Samples.background_samples + Samples.auxiliary_background_samples if 'qcdmu' not in s.name]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('GenHistos',
                       total_number_of_events = -1,
                       events_per_job = 20000,                    
                       scheduler = 'condor',
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*'
                       )
    #samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau1000um_M1000, Samples.mfv_neutralino_tau9900um_M0400, Samples.mfv_neutralino_tau9900um_M1000] + Samples.mfv_signal_samples
    if use_bkg:
        samples = []
        for s in Samples.myttbar_ali_samples:
            samples.append(s)
        for s in Samples.myttbar_tune_samples:
            samples.append(s)
    else:
        samples = [Samples.mysignal_tune_samples[0]]    
    cs.submit_all(samples)
