#!/usr/bin/env python

from functools import partial
from JMTucker.Tools.Sample import *

########################################################################

qcd_samples_not_used = [
    MCSample('qcdht0100', '/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',   81719052, nice='QCD, 100 < H_{T} < 200 GeV',   color=801, syst_frac=0.20, xsec=2.785e7),
    MCSample('qcdht0200', '/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',   18718905, nice='QCD, 200 < H_{T} < 300 GeV',   color=802, syst_frac=0.20, xsec=1.717e6),
    MCSample('qcdht0300', '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',   20278243, nice='QCD, 300 < H_{T} < 500 GeV',   color=803, syst_frac=0.20, xsec=3.513e5),
    ]

qcd_samples = [
    MCSample('qcdht0500', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  19701790, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 15547962, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 5085104, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 3952170, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  1981228, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

qcd_samples_ext = [
    MCSample('qcdht0500ext', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',   43242884, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700ext', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',  29569683, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000ext', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM', 10246203, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500ext', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',  7815090, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000ext', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',   4016332, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

# JMTBAD so the scripts downstream have an easy time
qcd_samples_sum = [ MCSample(x.name + 'sum', '/None/', x.nevents_orig + y.nevents_orig, nice=x.nice, color=x.color, syst_frac=x.syst_frac, xsec=x.xsec) for x,y in zip(qcd_samples, qcd_samples_ext) ]

# for x in 0500 0700 1000 1500 2000; hadd.py qcdht${x}sum.root qcdht${x}ext.root /uscms/home/tucker/jen/crab/HistosV6p1_76x_nstlays3_26/qcdht${x}.root

ttbar_samples = [
    MCSample('ttbar', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 38493485, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]

leptonic_background_samples = [
    MCSample('wjetstolnu',     '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',          24184766, nice='W + jets #rightarrow l#nu',                  color=  9, syst_frac=0.10, xsec=6.153e4), 
    MCSample('dyjetstollM10',  '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 30663441, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV',  color= 29, syst_frac=0.10, xsec=1.861e4),
    MCSample('dyjetstollM50',  '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM',     28827486, nice='DY + jets #rightarrow ll, M > 50 GeV',       color= 32, syst_frac=0.10, xsec=6.025e3),
    MCSample('qcdmupt15',      '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',    13247363, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=7.21e8 * 4.2e-4),
    ]

mfv_signal_samples = [
    MCSample('mfv_neu_tau00100um_M0300', '/mfv_neu_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0400', '/mfv_neu_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800', '/mfv_neu_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1200', '/mfv_neu_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1600', '/mfv_neu_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0300', '/mfv_neu_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0400', '/mfv_neu_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0800', '/mfv_neu_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1200', '/mfv_neu_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1600', '/mfv_neu_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0300', '/mfv_neu_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0400', '/mfv_neu_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0800', '/mfv_neu_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1200', '/mfv_neu_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1600', '/mfv_neu_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0300', '/mfv_neu_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0400', '/mfv_neu_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0800', '/mfv_neu_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1200', '/mfv_neu_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1600', '/mfv_neu_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    ]

mfv_signal_samples_glu = [
    MCSample('mfv_glu_tau00100um_M0300', '/mfv_glu_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M0400', '/mfv_glu_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M0800', '/mfv_glu_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M1200', '/mfv_glu_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M1600', '/mfv_glu_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M0300', '/mfv_glu_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M0400', '/mfv_glu_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M0800', '/mfv_glu_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M1200', '/mfv_glu_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M1600', '/mfv_glu_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M0300', '/mfv_glu_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M0400', '/mfv_glu_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M0800', '/mfv_glu_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M1200', '/mfv_glu_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M1600', '/mfv_glu_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M0300', '/mfv_glu_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M0400', '/mfv_glu_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M0800', '/mfv_glu_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M1200', '/mfv_glu_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M1600', '/mfv_glu_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    ]

mfv_signal_samples_gluddbar = [
    MCSample('mfv_gluddbar_tau00100um_M0300', '/mfv_gluddbar_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M0400', '/mfv_gluddbar_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M0800', '/mfv_gluddbar_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M1200', '/mfv_gluddbar_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M1600', '/mfv_gluddbar_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M0300', '/mfv_gluddbar_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M0400', '/mfv_gluddbar_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M0800', '/mfv_gluddbar_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M1200', '/mfv_gluddbar_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M1600', '/mfv_gluddbar_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M0300', '/mfv_gluddbar_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M0400', '/mfv_gluddbar_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M0800', '/mfv_gluddbar_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M1200', '/mfv_gluddbar_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M1600', '/mfv_gluddbar_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M0300', '/mfv_gluddbar_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M0400', '/mfv_gluddbar_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M0800', '/mfv_gluddbar_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M1200', '/mfv_gluddbar_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M1600', '/mfv_gluddbar_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    ]

mfv_signal_samples_lq2 = [
    MCSample('mfv_lq2_tau00100um_M0300', '/mfv_lq2_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M0400', '/mfv_lq2_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M0800', '/mfv_lq2_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M1200', '/mfv_lq2_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M1600', '/mfv_lq2_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M0300', '/mfv_lq2_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M0400', '/mfv_lq2_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M0800', '/mfv_lq2_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M1200', '/mfv_lq2_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M1600', '/mfv_lq2_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M0300', '/mfv_lq2_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M0400', '/mfv_lq2_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M0800', '/mfv_lq2_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M1200', '/mfv_lq2_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M1600', '/mfv_lq2_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M0300', '/mfv_lq2_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M0400', '/mfv_lq2_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M0800', '/mfv_lq2_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M1200', '/mfv_lq2_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M1600', '/mfv_lq2_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    ]

for s in mfv_signal_samples + mfv_signal_samples_glu + mfv_signal_samples_gluddbar + mfv_signal_samples_lq2:
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3
    s.aaa = us_aaa

xx4j_samples = [
    MCSample('xx4j_tau00001mm_M0050', '/XXTo4J_M-50_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      30000),
    MCSample('xx4j_tau00003mm_M0050', '/XXTo4J_M-50_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      29218),
    MCSample('xx4j_tau00010mm_M0050', '/XXTo4J_M-50_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     30000),
    MCSample('xx4j_tau00100mm_M0050', '/XXTo4J_M-50_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    29788),
    MCSample('xx4j_tau01000mm_M0050', '/XXTo4J_M-50_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   29316),
    MCSample('xx4j_tau02000mm_M0050', '/XXTo4J_M-50_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   30000),
    MCSample('xx4j_tau00001mm_M0100', '/XXTo4J_M-100_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     30000),
    MCSample('xx4j_tau00003mm_M0100', '/XXTo4J_M-100_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     30000),
    MCSample('xx4j_tau00010mm_M0100', '/XXTo4J_M-100_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    30000),
    MCSample('xx4j_tau00030mm_M0100', '/XXTo4J_M-100_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    30000),
    MCSample('xx4j_tau00100mm_M0100', '/XXTo4J_M-100_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   30000),
    MCSample('xx4j_tau00300mm_M0100', '/XXTo4J_M-100_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   30000),
    MCSample('xx4j_tau01000mm_M0100', '/XXTo4J_M-100_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  30000),
    MCSample('xx4j_tau02000mm_M0100', '/XXTo4J_M-100_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  30000),
    MCSample('xx4j_tau00001mm_M0300', '/XXTo4J_M-300_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00003mm_M0300', '/XXTo4J_M-300_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0300', '/XXTo4J_M-300_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0300', '/XXTo4J_M-300_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00100mm_M0300', '/XXTo4J_M-300_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M0300', '/XXTo4J_M-300_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau01000mm_M0300', '/XXTo4J_M-300_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau02000mm_M0300', '/XXTo4J_M-300_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00003mm_M0500', '/XXTo4J_M-500_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0500', '/XXTo4J_M-500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0500', '/XXTo4J_M-500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00300mm_M0500', '/XXTo4J_M-500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    9295),
    MCSample('xx4j_tau01000mm_M0500', '/XXTo4J_M-500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau02000mm_M0500', '/XXTo4J_M-500_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00001mm_M0700', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00003mm_M0700', '/XXTo4J_M-700_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0700', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0700', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00100mm_M0700', '/XXTo4J_M-700_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M0700', '/XXTo4J_M-700_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau01000mm_M0700', '/XXTo4J_M-700_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00001mm_M1000', '/XXTo4J_M-1000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00003mm_M1000', '/XXTo4J_M-1000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M1000', '/XXTo4J_M-1000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M1000', '/XXTo4J_M-1000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau01000mm_M1000', '/XXTo4J_M-1000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau02000mm_M1000', '/XXTo4J_M-1000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau00001mm_M1500', '/XXTo4J_M-1500_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9908),
    MCSample('xx4j_tau00010mm_M1500', '/XXTo4J_M-1500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00030mm_M1500', '/XXTo4J_M-1500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M1500', '/XXTo4J_M-1500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau01000mm_M1500', '/XXTo4J_M-1500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  9745),
    MCSample('xx4j_tau00001mm_M3000', '/XXTo4J_M-3000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9882),
    MCSample('xx4j_tau00003mm_M3000', '/XXTo4J_M-3000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00010mm_M3000', '/XXTo4J_M-3000_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00030mm_M3000', '/XXTo4J_M-3000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00100mm_M3000', '/XXTo4J_M-3000_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00300mm_M3000', '/XXTo4J_M-3000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   9384),
    MCSample('xx4j_tau01000mm_M3000', '/XXTo4J_M-3000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau02000mm_M3000', '/XXTo4J_M-3000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    ]

for s in xx4j_samples:
    s.xsec = 1e-3

wh_samples_4Tau = [
    MCSample('wh_4Tau_tau0000mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_4Tau_tau1000mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('wh_4Tau_tau0100mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19800),
    MCSample('wh_4Tau_tau0010mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_4Tau_tau0001mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19700),
    MCSample('wh_4Tau_tau0000mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19900),
    MCSample('wh_4Tau_tau1000mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19900),
    MCSample('wh_4Tau_tau0100mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_4Tau_tau0010mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('wh_4Tau_tau0001mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_4Tau_tau0000mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_4Tau_tau1000mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19900),
    MCSample('wh_4Tau_tau0100mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19800),
    MCSample('wh_4Tau_tau0010mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_4Tau_tau0001mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

wh_samples_bbbb = [
    MCSample('wh_bbbb_tau0000mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_bbbb_tau1000mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('wh_bbbb_tau0100mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_bbbb_tau0010mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_bbbb_tau0001mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_bbbb_tau0000mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('wh_bbbb_tau1000mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19900),
    MCSample('wh_bbbb_tau0100mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_bbbb_tau0010mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_bbbb_tau0001mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_bbbb_tau0000mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('wh_bbbb_tau1000mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('wh_bbbb_tau0100mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_bbbb_tau0010mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('wh_bbbb_tau0001mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

zh_samples_4Tau = [
    MCSample('zh_4Tau_tau0000mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19900),
    MCSample('zh_4Tau_tau1000mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_4Tau_tau0100mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19800),
    MCSample('zh_4Tau_tau0010mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_4Tau_tau0001mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19900),
    MCSample('zh_4Tau_tau0000mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19600),
    MCSample('zh_4Tau_tau0100mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_4Tau_tau0010mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('zh_4Tau_tau0001mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_4Tau_tau0000mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_4Tau_tau1000mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19700),
    MCSample('zh_4Tau_tau0100mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_4Tau_tau0010mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('zh_4Tau_tau0001mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

zh_samples_bbbb = [
    MCSample('zh_bbbb_tau0000mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('zh_bbbb_tau1000mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_bbbb_tau0100mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_bbbb_tau0010mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_bbbb_tau0001mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_bbbb_tau0000mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_bbbb_tau1000mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_bbbb_tau0100mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19900),
    MCSample('zh_bbbb_tau0010mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_bbbb_tau0001mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('zh_bbbb_tau0000mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_bbbb_tau1000mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_bbbb_tau0100mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_bbbb_tau0010mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_bbbb_tau0001mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

zh_samples_dddd = [
    MCSample('zh_dddd_tau0010mm_M25', '/ZH_HToSSTodddd_ZToLL_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000)
]

for s in wh_samples_4Tau + wh_samples_bbbb + zh_samples_4Tau + zh_samples_bbbb + zh_samples_dddd:
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3

auxiliary_background_samples = [
    MCSample('ttbaraux',  '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10235840, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]

qcdpt_samples_not_used =[
    MCSample('qcdpt0005', '/QCD_Pt_5to10_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      6991536, nice='QCD, 5 < #hat{p}_{T} < 10 GeV',      color=808, syst_frac=0.10, xsec=6.102e+10),
    MCSample('qcdpt0010', '/QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/AODSIM',     6842800, nice='QCD, 10 < #hat{p}_{T} < 15 GeV',     color=808, syst_frac=0.10, xsec=5.888e+09),
    MCSample('qcdpt0015', '/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    38425945, nice='QCD, 15 < #hat{p}_{T} < 30 GeV',     color=808, syst_frac=0.10, xsec=1.837e+09),
    MCSample('qcdpt0030', '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9808025, nice='QCD, 30 < #hat{p}_{T} < 50 GeV',     color=808, syst_frac=0.10, xsec=1.409e+08),
    MCSample('qcdpt0050', '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9775360, nice='QCD, 50 < #hat{p}_{T} < 80 GeV',     color=808, syst_frac=0.10, xsec=1.920e+07),
    MCSample('qcdpt0080', '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    6953590, nice='QCD, 80 < #hat{p}_{T} < 120 GeV',    color=808, syst_frac=0.10, xsec=2.763e+06),
    MCSample('qcdpt0120', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   6848223, nice='QCD, 120 < #hat{p}_{T} < 300 GeV',   color=808, syst_frac=0.10, xsec=4.711e+05),
    ]

qcdpt_samples = [
    MCSample('qcdpt0170', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   6918748, nice='QCD, 170 < #hat{p}_{T} < 300 GeV',   color=800, syst_frac=0.10, xsec=1.173e+05),
    MCSample('qcdpt0300', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   5968960, nice='QCD, 300 < #hat{p}_{T} < 470 GeV',   color=801, syst_frac=0.10, xsec=7.823e+03),
    MCSample('qcdpt0470', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   3977770, nice='QCD, 470 < #hat{p}_{T} < 600 GeV',   color=802, syst_frac=0.10, xsec=6.482e+02),
    MCSample('qcdpt0600', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   3979884, nice='QCD, 600 < #hat{p}_{T} < 800 GeV',   color=803, syst_frac=0.10, xsec=1.869e+02),
    MCSample('qcdpt0800', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  3973224, nice='QCD, 800 < #hat{p}_{T} < 1000 GeV',  color=804, syst_frac=0.10, xsec=3.229e+01),
    MCSample('qcdpt1000', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 2967947, nice='QCD, 1000 < #hat{p}_{T} < 1400 GeV', color=805, syst_frac=0.10, xsec=9.418e+00),
    MCSample('qcdpt1400', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  395725, nice='QCD, 1400 < #hat{p}_{T} < 1800 GeV', color=806, syst_frac=0.10, xsec=8.427e-01),
    MCSample('qcdpt1800', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  393760, nice='QCD, 1800 < #hat{p}_{T} < 2400 GeV', color=807, syst_frac=0.10, xsec=1.149e-01),
    MCSample('qcdpt2400', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  398452, nice='QCD, 2400 < #hat{p}_{T} < 3200 GeV', color=808, syst_frac=0.10, xsec=6.830e-03),
    MCSample('qcdpt3200', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   391108, nice='QCD, #hat{p}_{T} > 3200 GeV',        color=809, syst_frac=0.10, xsec=1.654e-04),
    ]

'''
These not updated for run2.

ttbar_systematics_samples = [
    MCSample('ttbarsystMSDecays', '', 999, nice='t#bar{t} (MSDecays)',                                       color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystM166p5',   '', 999, nice='t#bar{t} (M=166.5 GeV)',                                    color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystM178p5',   '', 999, nice='t#bar{t} (M=178.5 GeV)',                                    color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystMatchDn',  '', 999, nice='t#bar{t} (match down)',                                     color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystMatchUp',  '', 999, nice='t#bar{t} (match up)',                                       color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystScaleDn',  '', 999, nice='t#bar{t} (Q^2 down)',                                       color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystScaleUp',  '', 999, nice='t#bar{t} (Q^2 up)',                                         color=  4, syst_frac=0.15, xsec=888.),
    ]
'''

########################################################################

data_samples = [
    DataSample('JetHT2015D', '/JetHT/Run2015D-16Dec2015-v1/AOD'), # 256630 - 260727
    ]

auxiliary_data_samples = [
    #DataSample('SingleMuon2015Dv3', '/SingleMuon/Run2015D-PromptReco-v3/AOD'),
    #DataSample('SingleMuon2015Dv4', '/SingleMuon/Run2015D-PromptReco-v4/AOD'),
    ]

for s in data_samples + auxiliary_data_samples:
    s.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver.txt'

########################################################################

registry = SamplesRegistry()

__all__ = [
    'qcd_samples_not_used',
    'qcd_samples',
    'qcd_samples_ext',
    'qcd_samples_sum',
    'ttbar_samples',
    'mfv_signal_samples',
    'mfv_signal_samples_glu',
    'mfv_signal_samples_gluddbar',
    'mfv_signal_samples_lq2',
    'xx4j_samples',
    'wh_samples_4Tau',
    'wh_samples_bbbb',
    'zh_samples_4Tau',
    'zh_samples_bbbb',
    'zh_samples_dddd',
    'leptonic_background_samples',
#    'ttbar_systematics_samples',
    'auxiliary_background_samples',
    'qcdpt_samples_not_used',
    'qcdpt_samples',
    'data_samples',
    'auxiliary_data_samples',
    'registry',
    ]

for x in __all__:
    o = eval(x)
    if type(o) == list:
        registry.add_list(x,o)
        for sample in o:
            registry.add(sample)
            exec '%s = sample' % sample.name
            __all__.append(sample.name)

########################################################################

# Extra datasets and other overrides go here.

qcdht0500.aaa = eu_aaa
qcdht1000.aaa = us_aaa + eu_aaa 

# Can't add data datasets by primary (many have the same primary).
for sample in data_samples + auxiliary_data_samples:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))

#JetHT2015D.add_dataset('ntuplev6p1_76x_nstlays3', '/JetHT/dquach-ntuplev6p1_76x_data-1a10619cdc6042d141a5a3a54b840554/USER', dbs_inst='phys03') #, 7607820) # 1311 files

def add_dataset_by_primary(ds_name, dataset, nevents_orig, **kwargs):
    x = registry.by_primary_dataset(dataset.split('/')[1])
    if len(x) != 1:
        raise ValueError('could not find sample for %s by primary dataset: %r' % (dataset, x))
    sample = x[0]
    sample.add_dataset(ds_name, dataset, nevents_orig, **kwargs)

def add_dataset_phys03(sample, ds_name, dataset, nevents_orig, **kwargs):
    sample.add_dataset(ds_name, dataset, nevents_orig, dbs_inst='phys03', **kwargs)

_adbp = add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

# for x in $(<a.txt); echo _adbp3\(\'\', \'${x}\', $(dass 3 nevents $x)\) \# $(dass 3 file $x | wl) files

_adbp3('sim', '/mfv_neu_tau00100um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00100um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00100um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9800) # 49 files
_adbp3('sim', '/mfv_neu_tau00100um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9400) # 47 files
_adbp3('sim', '/mfv_neu_tau01000um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9800) # 49 files
_adbp3('sim', '/mfv_neu_tau01000um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau01000um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau01000um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau10000um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9600) # 48 files
_adbp3('sim', '/mfv_neu_tau10000um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau10000um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9600) # 48 files
_adbp3('sim', '/mfv_neu_tau10000um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9600) # 48 files

# can't use _adbp3 on qcds because of the -ext datasets that have same primary
add_dataset_phys03(qcdht0500,    'ntuplev9', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-4b0c72a3fdc564adcdc2c154c01482f7/USER',      45715)  # 100 files
add_dataset_phys03(qcdht0700,    'ntuplev9', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-4b2e4c70e8958e8fd45a5c679a1199a3/USER',   4408678)  # 203 files
add_dataset_phys03(qcdht1000,    'ntuplev9', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-3e1ea67c23fb08856e57091c1c5aaeba/USER',  5039738)  # 204 files
add_dataset_phys03(qcdht1500,    'ntuplev9', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-21ccd0dbba5eb6576ae41f31b2cc9c9c/USER',  3952153)  # 159 files
add_dataset_phys03(qcdht2000,    'ntuplev9', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-040ab1057163835875baffa48b2fa1a7/USER',   1981228)  # 80 files 

add_dataset_phys03(qcdht0500ext, 'ntuplev9', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-c0dbf8f7d74fe38621329d40c5876f3a/USER',     101204)  # 217 files
add_dataset_phys03(qcdht0700ext, 'ntuplev9', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-fc1016e3099c99941c2146b8ca65968c/USER',   8360131)  # 383 files
add_dataset_phys03(qcdht1000ext, 'ntuplev9', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-3bceaa54cb03c9d1a6573e168429e56a/USER', 10144907)  # 411 files
add_dataset_phys03(qcdht1500ext, 'ntuplev9', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-4cc30f68e9767f0e3fcb8982620dbe6a/USER',  7815041)  # 314 files
add_dataset_phys03(qcdht2000ext, 'ntuplev9', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev9-fea534cd4515e61314fe849606ff4938/USER',   4016331)  # 162 files

_adbp3('ntuplev9', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev9-166a600604c520a45fa2652c4ab0486a/USER', 1340689) # 193 files

_adbp3('ntuplev9', '/mfv_neu_tau00100um_M0800/tucker-ntuplev9-18313a78d966c2ede551c26bbb7cd6a6/USER', 9900) # 1 files
_adbp3('ntuplev9', '/mfv_neu_tau00300um_M0800/tucker-ntuplev9-f5ac07842dbce4d3f4503c75620a983b/USER', 9877) # 1 files
_adbp3('ntuplev9', '/mfv_neu_tau01000um_M0800/tucker-ntuplev9-0e5ba3624103221ccee5b192546f6f35/USER', 9883) # 1 files
_adbp3('ntuplev9', '/mfv_neu_tau10000um_M0800/tucker-ntuplev9-2ca30ad984fbc6013509895bd6706a2d/USER', 9794) # 1 files

_adbp3('ntuplev9', '/XXTo4J_M-300_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev9-c16034de6b15be76e79af64a452ab07a/USER',  4058) # 1 files
_adbp3('ntuplev9', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev9-0e24c0b7b0b6333f43188f45863b063d/USER',  9898) # 1 files
_adbp3('ntuplev9', '/XXTo4J_M-300_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev9-e87edf2dccd6167bb5544ad4ec39008e/USER', 3518) # 1 files
_adbp3('ntuplev9', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev9-e74553e8198c5ee291c2806df7144d3e/USER', 9867) # 1 files

########################################################################

if __name__ == '__main__':
    main(registry)

    if 0:
        from DBS import *
        for x in qcd_samples + ttbar_samples + smaller_background_samples:
            ds = x.datasets['miniaod'].dataset
            print ds
            print numevents_in_dataset(ds)

    if 0:
        for sample in qcd_samples + ttbar_samples:
            print "'%s': %.4e," % (sample.name, sample.datasets['ntuplev6p1'].nevents_orig / float(sample.nevents_orig))

    if 0:
        from DBS import *
        for x in qcd_samples_ext:
            ds = x.dataset
            print ds
            print x.name, numevents_in_dataset(ds)

    if 0:
        for x,y in zip(qcd_samples, qcd_samples_ext):
            print x.name, x.int_lumi_orig/1000, '->', (x.int_lumi_orig + y.int_lumi_orig)/1000

    if 0:
        f = open('a.txt', 'wt')
        for x in qcd_samples + qcd_samples_ext + ttbar_samples + mfv_signal_samples + leptonic_background_samples + auxiliary_background_samples + mfv_signal_samples_gluddbar + xx4j_samples:
            for y in ('main', 'ntuplev9'):
                try:
                    x.set_curr_dataset(y)
                except KeyError:
                    continue
                fns = x.filenames
                print len(fns)
                f.write('(%r, %r): (%i, %r),\n' % (x.name, y, len(fns), fns))
