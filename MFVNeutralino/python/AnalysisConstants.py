#!/usr/bin/env python

import os

for line in open(os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/interface/AnalysisConstants.h')):
    if '=' in line:
        exec line.strip() # lol
