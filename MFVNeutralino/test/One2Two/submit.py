#!/usr/bin/env python

import os, sys

# For ntracks in 5-8:
#     For svdist_cut in 0.02-0.05 in steps of 10 micron:
#         With and without replacement:
#             For phi_exp in (fit for), 1-5 in steps of 0.5:
#                 For signal contamination in None + (1x, 10x, 50x, 100x) * (100um, 300um, 1000um, 9900um)
#                     For seed in 0-1000:
#                         if signal_contam is None
#                             Test all the samples individually, with full statistics available.
#                             Test all the samples individually, sampling N_20ifb events in each pseudoexp.
#                             Test all the samples individually, sampling Pois(N_20ifb events) in each pseudoexp.
#                         With and without qcd500:
#                             Test all samples, sampling N_20ifb events in each pseudoexp.
#                             Test all samples, sampling Pois(N_20ifb events) in each pseudoexp.

script_template = '''#!/bin/tcsh
echo script starting on `date`
echo script args: $argv
echo wd: `pwd`

setenv JMT_WD `pwd`
setenv JOB_NUM $argv[1]

setenv SCRAM_ARCH slc5_amd64_gcc462
setenv JMT_CMSSW_VERSION CMSSW_5_3_13

source /uscmst1/prod/sw/cms/cshrc prod

echo trying to setup CMSSW $JMT_CMSSW_VERSION
scram project CMSSW $JMT_CMSSW_VERSION
cd $JMT_CMSSW_VERSION/src
cmsenv
echo ROOTSYS: $ROOTSYS
echo root-config: `root-config --libdir --version`
echo

echo set up libs
cd $CMSSW_BASE/lib/$SCRAM_ARCH
tar zxf $JMT_WD/lib.tgz
echo pwd `pwd`
echo ls -la
ls -la
echo

echo set up py
cd $CMSSW_BASE/src
tar zxvf $JMT_WD/py.tgz
mkdir $CMSSW_BASE/python/JMTucker
touch $CMSSW_BASE/python/JMTucker/__init__.py
cd $CMSSW_BASE/python/JMTucker
ln -s $CMSSW_BASE/src/JMTucker/Tools/python Tools
touch $CMSSW_BASE/python/JMTucker/Tools/__init__.py
echo PYTHONPATH $PYTHONPATH
echo pwd `pwd`
echo ls -laR
ls -laR
echo

echo untar trees
cd $JMT_WD
tar zxvf all_trees.tgz
echo

echo run one2two.py
cd $JMT_WD

setenv mfvo2t_job_num $JOB_NUM
setenv mfvo2t_seed $JOB_NUM
%(env)s

cmsRun one2two.py env >& out.$JOB_NUM
'''

jdl_template = '''universe = vanilla
Executable = runme.csh
arguments = $(Process)
Output = stdout.$(Cluster)_$(Process)
Error = stderr.$(Cluster)_$(Process)
Log = condor_log.$(Cluster)_$(Process)
stream_output = false
stream_error  = false
notification  = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = one2two.py, /uscms_data/d2/tucker/crab_dirs/mfv_535/MiniTreeV18/all_trees.tgz, lib.tgz, py.tgz
x509userproxy = $ENV(X509_USER_PROXY)
Queue %(njobs)s
'''

output_root = '/uscms/home/tucker/nobackup/One2Two'
os.system('mkdir -p ' + output_root)
os.system('cd $CMSSW_BASE/lib/* ; tar czf %s/lib.tgz * .edmplugincache ; cd - > /dev/null' % output_root)
os.system('cd $CMSSW_BASE/src/ ; tar czf %s/py.tgz JMTucker/Tools/python/Samples.py JMTucker/Tools/python/ROOTTools.py JMTucker/Tools/python/general.py JMTucker/Tools/python/DBS.py ; cd - > /dev/null' % output_root)

def submit(njobs, min_ntracks, svdist_cut, wrep, how_events, phi_exp, signal_contamination, samples):
    batch_name = 'Ntk%iSvd%sWrep%iHE%sPhi%sSC%sSam%s' % (min_ntracks,
                                                         ('%.3f' % svdist_cut).replace('.','p'),
                                                         int(wrep),
                                                         how_events,
                                                         'fit' if phi_exp is None else ('%.2f' % phi_exp).replace('.','p'),
                                                         'no' if signal_contamination is None else 'n%ix%i' % signal_contamination,
                                                         samples)

    batch_wd = os.path.join(output_root, batch_name)
    os.system('mkdir -p ' + batch_wd)
    old_wd = os.getcwd()
    os.chdir(batch_wd)

    os.system('cp %s/lib.tgz .' % output_root)
    os.system('cp %s/py.tgz .' % output_root)

    env = [
        'min_ntracks %i' % min_ntracks,
        'svdist2d_cut %f' % svdist2d_cut,
        'wrep %s' % (1 if wrep else "''"),
        ]

    if signal_contamination is not None:
        sig_samp, sig_scale = signal_contamination
        env.append('signal_contamination %i' % sig_samp)
        env.append('signal_scale %f' % sig_scale)

    if phi_exp is not None:
        env.append('phi_exp %f' % phi_exp)

    if 'full' in how_events:
        pass
    elif 'toy' in how_events:
        env.append('toy_mode 1')
        if 'pois' in how_events:
            env.append('poisson_n1vs 1')

    if 'all' in samples:
        env.append('sample all')
        if '500' in samples:
            env.append('use_qcd500 1')
    else:
        env.append('sample %s' % samples)

    env = '\n'.join('setenv mfvo2t_' + e for e in env)
    open('runme.csh', 'wt').write(script_template % {'env': env})
    open('runme.jdl', 'wt').write(jdl_template % {'njobs': njobs})

    os.chdir(old_wd)

submit(100, 5, 0.048, True, 'tbd', None, None, 'qcdht1000')

