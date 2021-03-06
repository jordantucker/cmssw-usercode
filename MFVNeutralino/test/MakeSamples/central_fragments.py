#!/usr/bin/env python

# JMTBAD keep in sync with modify.py

for_2018 = True

common = """
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP2Settings_cfi import *
"""
if for_2018:
    common += "from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *\n"
common += """
generator = cms.EDFilter('Pythia8GeneratorFilter',
    comEnergy = cms.double(13000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    SLHATableForPythia8 = cms.string(SLHA_TABLE),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP2SettingsBlock,"""
if for_2018:
    common += """
        pythia8PSweightsSettingsBlock,"""
common += """
        processParameters = cms.vstring(PROCESS_PARAMETERS),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP2Settings',"""
if for_2018:
    common += """
            'pythia8PSweightsSettings',"""
common += """
            'processParameters',
            ),
        ),
    )
"""

print common

def neu(fn, M, CTAU):
    f = open(fn, 'wt')
    f.write('M = %s\nCTAU = %s\n' % (M, CTAU))
    f.write(
"""
MGLU = M + 5.0
WIDTH = 0.0197e-11 / CTAU

SLHA_TABLE = '''
BLOCK SPINFO      # Spectrum calculator information
    1    Minimal  # spectrum calculator
    2    1.0.0    # version number

BLOCK MODSEL      # Model selection
    1    1        #

BLOCK MASS        # Mass Spectrum
#   PDG code   mass  particle
    1000021    %E    # ~g
    1000022    %E    # ~chi_10

DECAY    1000021    0.01E+0.00       # gluino decays
#   BR          NDA  ID1        ID2
    1.0E00      2    1000022    21   # BR(~g -> ~chi_10 g)

DECAY    1000022    %E               # neutralino decays
#   BR          NDA  ID1   ID2   ID3
    5.00E-01    3     3     5     6  # BR(~chi_10 -> s    b    t)
    5.00E-01    3    -3    -5    -6  # BR(~chi_10 -> sbar bbar tbar)
''' % (MGLU, M, WIDTH)

""" + common.replace("PROCESS_PARAMETERS","""
            'SUSY:gg2gluinogluino = on',
            'SUSY:qqbar2gluinogluino = on',
            'SUSY:idA = 1000021',
            'SUSY:idB = 1000021',
            '1000022:tau0 = %f' % CTAU,
            """))

def stop(fn, M, CTAU):
    f = open(fn, 'wt')
    f.write('M = %s\nCTAU = %s\n' % (M, CTAU))
    f.write(
"""
WIDTH = 0.0197e-11 / CTAU

SLHA_TABLE = '''
BLOCK SPINFO      # Spectrum calculator information
    1    Minimal  # spectrum calculator
    2    1.0.0    # version number

BLOCK MODSEL      # Model selection
    1    1        #

BLOCK MASS        # Mass Spectrum
#   PDG code   mass  particle
    1000006    %E    # ~t_1

DECAY    1000006    %E               # ~t_1 decays (~t_1bar is automatically handled)
#   BR          NDA  ID1   ID2
    1.00E+00    2    -1    -1        # ~t_1 -> dbar dbar
''' % (M, WIDTH)

""" + common.replace("PROCESS_PARAMETERS","""
            'SUSY:all = off',
            'SUSY:gg2squarkantisquark = on',
            'SUSY:qqbar2squarkantisquark = on',
            'SUSY:idA = 1000006',
            'SUSY:idB = 1000006',
            'RHadrons:allow = on',
            '1000006:tau0 = %f' % CTAU,
            """))

for model in neu, stop:
    if model == neu:
        samplebase = 'GluinoGluinoToNeutralinoNeutralinoTo2T2B2S'
    elif model == stop:
        samplebase = 'StopStopbarTo2Dbar2D'
    for ctau, ctauname in (0.1, '100um'), (0.3, '300um'), (1., '1mm'), (10., '10mm'), (30., '30mm'):
        for m in 200, 300, 400, 600, 800, 1200, 1600, 2400, 3000:
            sample = samplebase + '_M-%i_CTau-%s_TuneCP2_13TeV-pythia8' % (m, ctauname)
            fn = sample.replace('-', '_') + '_cff.py'
            print '%s,100000,%s,pythia8' % (sample, fn)
            model(fn, m, ctau)
