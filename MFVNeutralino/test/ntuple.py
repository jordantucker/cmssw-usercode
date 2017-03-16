#!/usr/bin/env python

from JMTucker.Tools.MiniAOD_cfg import cms, pat_tuple_process
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

is_mc = True
prepare_vis = False
keep_all = prepare_vis
trig_filter = not keep_all
version = 'v11'
batch_name = 'Ntuple' + version.upper()
#batch_name += '_ChangeMeIfSettingsNotDefault'

####

def customize_before_unscheduled(process):
    process.load('JMTucker.MFVNeutralino.Vertexer_cff')
    process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
    process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

    process.p = cms.Path(process.mfvVertexSequence * cms.ignore(process.mfvTriggerFloats) * process.mfvEvent)

    tfileservice(process, 'vertex_histos.root')
    random_service(process, {'mfvVertices': 1222})

    process.out.outputCommands = output_commands = [
        'drop *',
        'keep *_mcStat_*_*',
        'keep MFVVertexAuxs_mfvVerticesAux_*_*',
        'keep MFVEvent_mfvEvent__*',
        ]

    if prepare_vis:
        process.mfvSelectedVerticesTight.produce_vertices = True
        process.mfvSelectedVerticesTight.produce_tracks = True

        process.load('JMTucker.MFVNeutralino.VertexRefitter_cfi')
        process.mfvVertexRefitsDrop0 = process.mfvVertexRefits.clone(n_tracks_to_drop = 0)
        process.mfvVertexRefitsDrop2 = process.mfvVertexRefits.clone(n_tracks_to_drop = 2)
        process.p *= process.mfvVertexRefits * process.mfvVertexRefitsDrop2 *  process.mfvVertexRefitsDrop0

        output_commands += [
            'keep *_mfvVertices_*_*',
            'keep *_mfvSelectedVerticesTight_*_*',
            'keep *_mfvVertexRefits_*_*',
            'keep *_mfvVertexRefitsDrop2_*_*',
            'keep *_mfvVertexRefitsDrop0_*_*',
            ]

        if is_mc:
            process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                                     gen_particles_src = cms.InputTag('genParticles'),
                                                     print_info = cms.bool(True),
                                                     )
            process.p *= process.mfvGenParticles
            output_commands += ['keep *_mfvGenParticles_*_*']

    if keep_all:
        process.mfvEvent.skip_event_filter = ''

        def dedrop(l):
            return [x for x in l if not x.strip().startswith('drop')]
        if is_mc:
            process.out.outputCommands += \
                process.AODSIMEventContent.outputCommands + \
                dedrop(process.MINIAODSIMEventContent.outputCommands) + \
                dedrop(output_commands)
        else:
            process.out.outputCommands += \
                process.AODEventContent.outputCommands + \
                dedrop(process.MINIAODEventContent.outputCommands) + \
                dedrop(output_commands)
        # for some reason taus crash with this cfg in 8025, and you have to drop met too then (then have to kill it in EventProducer)
        process.mfvEvent.met_src = ''
        process.out.outputCommands = [x for x in process.out.outputCommands if 'tau' not in x.lower() and 'MET' not in x]
        for x in dir(process):
            xl = x.lower()
            if 'tau' in xl or 'MET' in x:
                delattr(process, x)

process = pat_tuple_process(customize_before_unscheduled, is_mc, year)
process.out.fileName = 'ntuple.root'

process.out.outputCommands += [
    # these three get added to the end
    'drop patMETs_patPFMetPuppi__PAT',
    'drop patMETs_patCaloMet__PAT',
    'drop patMETs_patMETPuppi__PAT',
    ]

if is_mc:
    process.mcStat.histos = True

# If the embedding is on for these, then we can't match leptons by track to vertices.
process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False

if trig_filter:
    import JMTucker.MFVNeutralino.TriggerFilter
    JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)
else:
    process.mfvEvent.skip_event_filter = ''

#process.options.wantSummary = True
process.maxEvents.input = 100
file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    if year == 2015:
        samples = \
            Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            Samples.mfv_signal_samples_2015 + Samples.mfv_signal_samples_glu_2015 + Samples.mfv_signal_samples_gluddbar_2015 + Samples.xx4j_samples_2015
    elif year == 2016:
        samples = \
            Samples.data_samples + \
            Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
            Samples.official_mfv_signal_samples

    filter_eff = { 'qcdht0500': 2.9065e-03, 'qcdht0700': 3.2294e-01, 'qcdht0500ext': 2.9065e-03, 'qcdht0700ext': 3.2294e-01, 'ttbar': 3.6064e-02, 'ttbaraux': 3.6064e-02, 'qcdpt0120': 3.500e-05, 'qcdpt0170': 7.856e-03, 'qcdpt0300': 2.918e-01 }
    for s in samples:
        s.files_per = 5
        if s.is_mc and filter_eff.has_key(s.name):
            s.events_per = min(int(25000/filter_eff[s.name]), 200000)

    from JMTucker.Tools.MetaSubmitter import *
    skips = {
        'qcdht0700ext': {'lumis': '135728', 'events': '401297681'},
        'qcdht1000ext': {'lumis': '32328',  'events': '108237235'},
        }
    modify = chain_modifiers(is_mc_modifier, event_veto_modifier(skips))
    ms = MetaSubmitter(batch_name + '/%i' % year)
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
