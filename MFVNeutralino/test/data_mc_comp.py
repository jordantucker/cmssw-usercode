#!/usr/bin/env python

import os
from functools import partial
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver

root_file_dir = '/uscms_data/d3/dquach/crab3dirs/HistosV3_newcuts_sigmadxy3p0'
plot_dir = 'plots/HistosV3_sigmadxy3p0_pretty_data_mc_comp'

set_style()
ps = plot_saver(plot_dir)

scale_factor = 1.

data_samples = [] # Samples.data_samples
background_samples = Samples.ttbar_samples + Samples.qcd_samples[3:]
signal_samples = [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]
y= ['100 #mum, #sigma = 100 fb', '300 #mum, #sigma = 5 fb', '1 mm, #sigma = 1 fb', '10 mm, #sigma = 1 fb']
c=[2,4,6,8]
s=[0.1,0.005,0.001, 0.001]
for i, signal_sample in enumerate(signal_samples):
    signal_sample.xsec = s[i]
    signal_sample.nice_name = '#tau = %s' % y[i]
    signal_sample.color = c[i]

for s in Samples.qcd_samples:
    s.join_info = True, 'Multi-jet events', ROOT.kBlue-9
for s in Samples.ttbar_samples: # + Samples.smaller_background_samples + Samples.leptonic_background_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7 #, single t, V+jets, t#bar{t}+V, VV', ROOT.kBlue-7

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = ac.int_lumi * scale_factor, 
            int_lumi_nice = ac.int_lumi_nice,
            #background_uncertainty = ('Uncert. on MC bkg', 0.2, ROOT.kBlack, 3004),
            canvas_top_margin = 0.08,
            overflow_in_last = True,
            poisson_intervals = True,
            enable_legend = True,
            legend_pos = (0.350, 0.635, 0.869, 0.843),
            res_fit = True,
            verbose = True,
            )

C('nsv',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  x_title = 'number of vertices',
  y_title = 'events',
  x_range = (0,5),
  y_range = (1, 3e6),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((2, 0, 2, 6.4e6), 5, 5, 1),
  )

#dbv_bins = [j*0.005 for j in range(8)] + [0.04, 0.05, 0.06, 0.07, 0.085, 0.1]
#
#C('dbv',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
#  rebin = dbv_bins,
#  bin_width_to = 0.005,
#  x_title = 'd_{BV} (cm)',
#  y_title = 'vertices/50 #mum',
#  x_range = (0,0.3),
#  y_range = (0.5, 33000),
#  y_title_offset = 1.19,
#  res_y_range = (0,2.5),
#  )
#
dvv_bins = [j*0.01 for j in range(21)] # + [0.2]

C('dvv',
  histogram_path = 'mfvVertexHistosWAnaCuts/h_svdist2d',
  x_title = 'd_{VV} (cm)',
  y_title = 'events/100 #mum',
  rebin = dvv_bins,
  #bin_width_to = 0.01,
  y_title_offset = 1.19,
  res_y_range = (0, 10),
  y_range = (0.005, 100),
  )

#enabled = [x.strip() for x in '''
#npv
#jetsumht
#nsv
#sv_all_ntracks_nm1
#sv_all_ntracksptgt3_nm1
#sv_all_drmin_nm1
#sv_all_maxdrmax_nm1
#sv_all_mindrmax_nm1
#sv_all_njetsntks_nm1
#sv_all_bsbs2ddist
#sv_all_bs2derr_nm1
#sv_all_svdist2d
#'''.split('\n') if not x.strip().startswith('#')]
#
#def is_enabled(s):
#    return s in enabled # or s.startswith('clean')
#
#def D(*args, **kwargs):
#    if is_enabled(args[0]):
#        C(*args, **kwargs)
#
#def event_histo(h):
#    return 'mfvEventHistos/' + h
#
#D('npv',
#  histogram_path = event_histo('h_npv'),
#  x_title = 'number of PV',
#  y_title = 'events/2',
#  x_range = (0, 40),
#  rebin = 2,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('ncalojets',
#  histogram_path = event_histo('h_ncalojets'),
#  x_title = 'number of calorimeter jets',
#  y_title = 'events',
#  x_range = (3,16),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('calojetpt1',
#  histogram_path = event_histo('h_calojetpt1'),
#  x_title = 'calorimeter jet #1 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  x_range = (50,500),
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('calojetpt2',
#  histogram_path = event_histo('h_calojetpt2'),
#  x_title = 'calorimeter jet #2 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  x_range = (50,500),
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('calojetpt3',
#  histogram_path = event_histo('h_calojetpt3'),
#  x_title = 'calorimeter jet #3 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  x_range = (50,500),
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('calojetpt4',
#  histogram_path = event_histo('h_calojetpt4'),
#  x_title = 'calorimeter jet #4 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  x_range = (50,250),
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('calojetpt5',
#  histogram_path = event_histo('h_calojetpt5'),
#  x_title = 'calorimeter jet #5 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  x_range = (0,250),
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('npfjets',
#  histogram_path = event_histo('h_njets'),
#  x_title = 'number of particle-flow jets',
#  y_title = 'events',
#  x_range = (3,16),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('pfjetpt1',
#  histogram_path = event_histo('h_jetpt1'),
#  x_title = 'particle-flow jet #1 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('pfjetpt2',
#  histogram_path = event_histo('h_jetpt2'),
#  x_title = 'particle-flow jet #2 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('pfjetpt3',
#  histogram_path = event_histo('h_jetpt3'),
#  x_title = 'particle-flow jet #3 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('pfjetpt4',
#  histogram_path = event_histo('h_jetpt4'),
#  x_title = 'particle-flow jet #4 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  x_range = (0,250),
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('pfjetpt5',
#  histogram_path = event_histo('h_jetpt5'),
#  x_title = 'particle-flow jet #5 p_{T} (GeV)',
#  y_title = 'events/20 GeV',
#  x_range = (0,250),
#  rebin = 4,
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('jetsumht',
#  histogram_path = event_histo('h_jet_sum_ht'),
#  rebin = 5,
#  x_title = 'particle-flow jet #Sigma H_{T} (GeV)',
#  y_title = 'events/100 GeV',
#  x_range = (400, 3000),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('sv_best0_ntracks_nm1',
#  histogram_path = 'vtxHstOnly1VNoNtracks/h_sv_best0_ntracks',
#  x_title = 'number of tracks/vertex',
#  y_title = 'vertices',
#  x_range = (2, 20),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  cut_line = ((5.,0.0,5.,52200),ROOT.kRed,5,1),
#  )
#
#D('sv_best0_ntracksptgt3_nm1',
#  histogram_path = 'vtxHstOnly1VNoNtracksptgt3/h_sv_best0_ntracksptgt3',
#  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
#  y_title = 'vertices',
#  x_range = (0, 9),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  cut_line = ((3.,0.0,3.,380000),ROOT.kRed,5,1),
#  )
#
#D('sv_best0_drmin_nm1',
#  histogram_path = 'vtxHstOnly1VNoDrmin/h_sv_best0_drmin',
#  rebin = 4,
#  x_title = 'min{#Delta R{track i,j}}',
#  y_title = 'vertices/0.04',
#  x_range = (0, 0.6),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  cut_line = ((0.4,0.0,0.4,67700),ROOT.kRed,5,1),
#  )
#
#D('sv_best0_drmax_nm1',
#  histogram_path = 'vtxHstOnly1VNoDrmax/h_sv_best0_drmax',
#  rebin = 6,
#  x_title = 'max{#Delta R{track i,j}}',
#  y_title = 'vertices/0.28',
#  legend_pos = (0.13, 0.70, 0.43, 0.90),
#  cut_line = ((4,0.0,4,71800),ROOT.kRed,5,1),
#  )
#
#D('sv_best0_njetsntks_nm1',
#  histogram_path = 'vtxHstOnly1VNoNjets/h_sv_best0_njetsntks',
#  x_title = 'number of associated jets',
#  y_title = 'vertices',
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  cut_line = ((1.,0.0,1.,128000),ROOT.kRed,5,1),
#  )
#
#D('sv_best0_bsbs2ddist',
#  histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_best0_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'vertices/50 #mum',
#  x_range = (0, 0.1),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  )
#
#D('sv_best0_bs2derr_nm1',
#  histogram_path = 'vtxHstOnly1VNoBs2derr/h_sv_best0_bs2derr',
#  x_title = '#sigma(d_{BV}) (cm)',
#  y_title = 'vertices/5 #mum',
#  x_range = (0, 0.01),
#  legend_pos = (0.47, 0.70, 0.87, 0.90),
#  cut_line = ((0.0025,0.0,0.0025,148000),ROOT.kRed,5,1),
#  )
#
#D('sv_best0_jets_deltaphi',
#  histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_best0_jets_deltaphi',
#  x_title = '#Delta#phi_{JV}',
#  y_title = 'jet-vertex pairs/0.252',
#  y_range = (None,1e5),
#  legend_pos = (0.47, 0.78, 0.87, 0.93),
#  rebin = 2,
#  )
#
#################################################################################
#
#D('calojetpt4_nocuts',
#  histogram_path = 'mfvEventHistosNoCuts/h_calojetpt4',
#  x_title = 'calorimeter jet #4 p_{T} (GeV)',
#  y_title = 'events/10 GeV',
#  x_range = (0,250),
#  rebin = 2,
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  cut_line = ((60, 0, 60, 205e6), 2, 5, 1),
#  )
#
#D('jetsumht_nocuts',
#  histogram_path = 'mfvEventHistosNoCuts/h_jet_sum_ht',
#  rebin = 4,
#  x_title = 'particle-flow jet #Sigma H_{T} (GeV)',
#  y_title = 'events/100 GeV',
#  x_range = (0, 3000),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  cut_line = ((500, 0, 500, 200e6), 2, 5, 1),
#  )
#
#D('nsv',
#  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
#  x_title = 'number of vertices',
#  y_title = 'events',
#  x_range = (0,5),
#  y_range = (1, 3e6),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  cut_line = ((2, 0, 2, 3e6), 2, 5, 1),
#  )
#
#D('sv_all_ntracks_nm1',
#  histogram_path = 'vtxHst2VNoNtracks/h_sv_all_ntracks',
#  x_title = 'number of tracks/vertex',
#  y_title = 'vertices',
#  x_range = (0,25),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  cut_line = ((5, 0, 5, 1000), 2, 5, 1),
#  )
#
#D('sv_all_ntracksptgt3_nm1',
#  histogram_path = 'vtxHst2VNoNtracksptgt3/h_sv_all_ntracksptgt3',
#  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
#  y_title = 'vertices',
#  x_range = (0, 20),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  cut_line = ((3, 0, 3, 40), 2, 5, 1),
#  )
#
#D('sv_all_tksjetsntkmass',
#  histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_all_tksjetsntkmass',
#  rebin = 6,
#  x_title = 'tracks + associated jets\' mass (GeV)',
#  y_title = 'vertices/90 GeV',
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  )
#
#D('sv_all_drmin_nm1',
#  histogram_path = 'vtxHst2VNoDrmin/h_sv_all_drmin',
#  x_title = 'min{#Delta R{track i,j}}',
#  y_title = 'vertices/0.08',
#  rebin = 8,
#  cut_line = ((0.4, 0, 0.4, 70), 2, 5, 1),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  )
#
#D('sv_all_maxdrmax_nm1',
#  histogram_path = 'vtxHst2VNoDrmax/h_sv_all_drmax',
#  rebin = 6,
#  x_title = 'max{#Delta R{track i,j}}',
#  y_title = 'vertices/0.28',
#  cut_line = ((4, 0, 4, 33), 2, 5, 1),
#  legend_pos = (0.13, 0.70, 0.43, 0.90),
#  )
#
#D('sv_all_mindrmax_nm1',
#  histogram_path = 'vtxHst2VNoMindrmax/h_sv_all_drmax',
#  rebin = 6,
#  x_title = 'max{#Delta R{track i,j}}',
#  y_title = 'vertices/0.28',
#  x_range = (0,5),
#  cut_line = ((1.2, 0, 1.2, 31), 2, 5, 1),
#  legend_pos = (0.13, 0.70, 0.43, 0.90),
#  )
#
#D('sv_all_njetsntks_nm1',
#  histogram_path = 'vtxHst2VNoNjets/h_sv_all_njetsntks',
#  x_title = 'number of associated jets',
#  y_title = 'vertices',
#  x_range = (0,10),
#  cut_line = ((1, 0, 1, 40), 2, 5, 1),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  )
#
#D('sv_all_bsbs2ddist',
#  histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'vertices/50 #mum',
#  x_range = (0, 0.3),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  )
#
#D('sv_all_bs2derr_nm1',
#  histogram_path = 'vtxHst2VNoBs2derr/h_sv_all_bs2derr',
#  x_title = '#sigma(d_{BV}) (cm)',
#  y_title = 'vertices/5 #mum',
#  x_range = (0, 0.015),
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  cut_line = ((0.0025, 0, 0.0025, 60), 2, 5, 1),
#  )
#
#D('sv_all_svdist2d',
#  histogram_path = 'mfvVertexHistosWAnaCuts/h_svdist2d',
#  x_title = 'd_{VV} (cm)',
#  y_title = 'events/0.01 cm',
#  x_range = (0,0.13),
#  rebin = 10,
#  legend_pos = (0.47, 0.67, 0.87, 0.87),
#  )
