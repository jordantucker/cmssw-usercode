import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, file_event_from_argv, process

simple = False

process.source.fileNames = ['root://osg-se.cac.cornell.edu//xrootd/path/cms/store/user/tucker/mfv_hltrun2_M0400/patpu40/150626_223437/0000/pat_1.root']
process.TFileService.fileName = 'histos.root'
process.maxEvents.input = 100
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.Histos_cff')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

nm1s = [
    ('Ntracks', 'min_ntracks = 0, min_njetsntks = 0'),
    ('Drmin',   'max_drmin = 1e9'),
    ('Geo2d',   'max_geo2ddist = 1e9'),
    ('Bs2derr', 'max_bs2derr = 1e9'),
    ('Njets',   'min_njetsntks = 0'),
    ]

if simple:
    nm1s = []

    del process.pFullSel
    del process.pOnlyOneVtx
    del process.pPreSel
    del process.pSkimSel
    del process.pSigReg

    process.p = cms.Path(process.mfvSelectedVerticesLoose +
                         process.mfvSelectedVerticesTight +
                         process.mfvWeight +
                         process.mfvEventHistosNoCuts +
                         process.mfvVertexHistosNoCuts +
                         process.mfvVertexHistos +
                         process.mfvAnalysisCuts +
                         process.mfvEventHistos +
                         process.mfvVertexHistosWAnaCuts)

for name, cut in nm1s:
    evt_cut = ''
    if type(cut) == tuple:
        cut, evt_cut = cut

    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name

    for nv in (1,2):
        ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
        ana.vertex_src = vtx_name
        ana.max_nvertex = nv
        ana.min_nvertex = nv
        ana_name = 'ana%iVNo' % nv + name

        evt_hst = process.mfvEventHistos.clone()
        evt_hst_name = 'evtHst%iVNo' % nv + name

        vtx_hst = process.mfvVertexHistos.clone(vertex_aux_src = vtx_name)
        vtx_hst_name = 'vtxHst%iVNo' % nv + name

        setattr(process, vtx_name, vtx)
        setattr(process, ana_name, ana)
        setattr(process, evt_hst_name, evt_hst)
        setattr(process, vtx_hst_name, vtx_hst)
        setattr(process, 'p%iV' % nv + name, cms.Path(vtx * ana * evt_hst * vtx_hst))

def force_bs(process, bs):
    for ana in process.analyzers:
        if hasattr(ana, 'force_bs'):
            ana.force_bs = bs

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        Samples.xx4j_samples

    for sample in Samples.data_samples:
        sample.json = 'ana_10pc.json'
        sample.lumis_per = 200

    cs = CRABSubmitter('HistosV6p1',
                       dataset = 'ntuplev6p1',
                       job_control_from_sample = True,
                       aaa = True, # stored at FNAL, easy to run on T2_USes
                       )
    cs.submit_all(samples)
