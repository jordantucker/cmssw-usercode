#!/usr/bin/env python

raise ValueError('understand/backport pythia variations--see central_fragments.py for 2018 and http://home.thep.lu.se/Pythia/pythia82html/Variations.html')

import os
from JMTucker.Tools.Year import year; assert year == 2017
from scanpack import get_scanpack, scanpackbase

condor = False
nevents = 10000
events_per = 100
expected_events_frac = 1.
scanpack = None
output_level = 'reco'
output_dataset_tag = ''
fixed_salt = ''
use_this_cmssw = False
premix = True
trig_filter = False
hip_simulation = False
hip_mitigation = False
ex = ''

meta = 'neu'
taus   = [100, 300, 1000, 10000, 30000, 100000]
masses = [200, 300, 400, 600, 800, 1200, 1600, 3000] if meta.startswith('neu') else [400, 600, 800, 1200, 1600, 3000]
tau_masses = [] # [(1000,800),(30000,800),(1000,1600),(30000,1600),(1000,3000),(30000,3000)]
already = []
hip_right = False

if 0:
    meta = 'scan'
    output_level = 'minitree'
    hip_right = False
    scanpack = 'scanpack3_' + os.environ['USER']
elif 0:
    meta = 'ttbar'
    nevents, events_per
    output_level = 'minitree'
elif 0:
    meta = 'minbias'
    nevents, events_per = 999000, 3000
    output_level = 'gensim'
    output_dataset_tag = 'RunIISummer15GS-MCRUN2_71_V1'
elif 0:
    meta = 'qcdht2000'
    nevents, events_per = 10000, 500
    expected_events_frac = 0.09  # JMTBAD
    output_level = 'gensim'
    output_dataset_tag = 'RunIIFall17wmLHEGS-93X_mc2017_realistic_v3'
elif 0:
    meta = 'qcdht1500'
    fixed_salt = 'fixedsalt'
    nevents, events_per = 200000, 1000 # 0.06 eff at gen matching with lhe events for 1000, more like 0.025 for 700
    expected_events_frac = 0.09  # JMTBAD
    if meta.endswith('0700'):
        nevents *= 14
    trig_filter = True
    hip_simulation = 1.0
    hip_mitigation = True
    ex = ''

####

if hip_right:
    hip_simulation = 1.0
    hip_mitigation = True

if hip_simulation:
    use_this_cmssw = True
    premix = False
    exx = '%.1f' % hip_simulation
    ex += '_hip' + exx.replace('.','p')
    if hip_mitigation:
        ex += '_mit'
else:
    hip_mitigation = False

if scanpack:
    ex += '_' + scanpack
    scanpack = get_scanpack(scanpack)

#ex = '_test'
#nevents, events_per = 5,5
#meta, taus, masses = 'stopdbardbar', [1000], [1200]

################################################################################

if output_level not in ('reco', 'ntuple', 'minitree', 'gensim'):
    raise ValueError('output_level %s not supported' % output_level)

import sys, os
from math import ceil
from pprint import pprint
from textwrap import dedent
from time import time
from CRABClient.ClientExceptions import ConfigException as CRABConfigException
from JMTucker.Tools.CRAB3Tools import Config, crab_dirs_root, crab_command
from JMTucker.Tools.general import index_startswith, save_git_status
from JMTucker.Tools.CondorSubmitter import CondorSubmitter
from JMTucker.Tools.Sample import MCSample
from JMTucker.Tools import colors

testing = 'testing' in sys.argv
work_area = crab_dirs_root('nstep_%s%s' % (meta, ex))
if os.path.isdir(work_area):
    sys.exit('work_area %s exists' % work_area)
os.makedirs(work_area)
gitstatus_dir = 'gitstatus_%s' % int(time()*1000)
if not condor:
    save_git_status(os.path.join(work_area, gitstatus_dir))

config = Config()

open('year.txt', 'wt').write(str(year))

to_rm = ['year.txt']

if output_level in ('minitree', 'ntuple'):
    for x in 'ntuple.py', 'minitree.py':
        to_rm.append(x)
        os.system('cmsDumpPython.py ../%s > %s' % (x,x))

config.General.transferLogs = False
config.General.transferOutputs = True
config.General.workArea = work_area
config.General.requestName = 'SETME'

config.JobType.pluginName = 'PrivateMC'
dummy_pset_fn_orig = 'dummy.py'
dummy_pset_fn_temp = config.JobType.psetName = 'tmpdummy.py'
to_rm.append(dummy_pset_fn_temp)
config.JobType.scriptExe = 'nstep.sh'
config.JobType.scriptArgs = []
config.JobType.sendPythonFolder = True
config.JobType.maxMemoryMB = 3000

steering_fn = 'steering.sh'

config.JobType.inputFiles = ['todoify.sh', steering_fn, 'gensim.py', 'dynamicconf.py', 'modify.py', 'scanpack.py', 'rawhlt.py', 'minbias.py', 'minbias_premix.txt.gz', 'reco.py', 'fixfjr.py', 'year.txt']
if output_level in ('minitree', 'ntuple'):
    config.JobType.inputFiles += ['ntuple.py', 'minitree.py']

output_is_edm = True
if output_level == 'reco':
    output_fn = 'reco.root'
elif output_level == 'gensim':
    output_fn = 'gensim.root'
elif output_level == 'ntuple':
    output_fn = 'ntuple.root'
elif output_level == 'minitree':
    output_fn = 'minitree.root'
    output_is_edm = False
config.JobType.outputFiles = [output_fn]

dummy_pset = open(dummy_pset_fn_orig).read()
if output_is_edm:
    to_rep = 'reco.root', output_fn
else:
    to_rep = 'if True: # EDM output hack', 'if False:'
assert to_rep[0] in dummy_pset
open(dummy_pset_fn_temp, 'wt').write(dummy_pset.replace(*to_rep))

# uncomment to get vertex histos
#if output_level in ('minitree', 'ntuple'):
#    config.JobType.outputFiles += ['vertex_histos.root']

config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = events_per
config.Data.totalUnits = nevents
config.Data.publication = output_level not in ('minitree', 'ntuple')
config.Data.outputPrimaryDataset = 'SETME'
if output_dataset_tag == '':
    if premix:
        output_dataset_tag = 'RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1'
    else:
        raise NotImplementedError('premix')
        output_dataset_tag = ''
config.Data.outputDatasetTag = output_dataset_tag

config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.whitelist = ['T1_US_FNAL', 'T2_US_MIT', 'T2_US_Nebraska', 'T2_US_Purdue', 'T2_US_UCSD', 'T2_US_Wisconsin', 'T2_US_Vanderbilt', 'T2_US_Caltech', 'T2_US_Florida', 'T2_CH_CERN', 'T2_DE_DESY']
if output_level == 'gensim':
    config.Site.whitelist += ['T3_US_*']

outputs = {}

def submit(config, name, scanpack_or_todo, todo_rawhlt=[], todo_reco=[], todo_ntuple=[]):
    global nevents
    global events_per

    config.General.requestName = name
    config.Data.outputPrimaryDataset = name

    if isinstance(scanpack_or_todo, scanpackbase):
        scanpack, todo = scanpack_or_todo, None
    else:
        scanpack, todo = None, scanpack_or_todo

    if scanpack:
        nevents = config.Data.totalUnits = scanpack.nevents
        events_per = config.Data.unitsPerJob = scanpack.events_per_job

    dummy_for_hash = int(time()*1e6)
    steering = [
        'MAXEVENTS=%i' % events_per,
        'EXPECTEDEVENTS=%i' % ceil(events_per*expected_events_frac),
        'USETHISCMSSW=%i' % use_this_cmssw,
        'TRIGFILTER=%i' % trig_filter,
        'PREMIX=%i' % premix,
        'export DUMMYFORHASH=%i' % dummy_for_hash,  # exported so the python script executed in cmsRun can just get it from os.environ instead of parsing argv like we do the rest
        'OUTPUTLEVEL=%s' % output_level,
        ]

    if todo:
        steering.append('TODO=todo=' + todo)

    if scanpack:
        steering.append('SCANPACK=scanpack=%s,%s' % (scanpack.name, scanpack.ibatch))

    salt = fixed_salt
    if not fixed_salt:
        salt = '%s %s' % (name, todo)
        if scanpack:
            salt += ' ' + scanpack.batch_name

    if hip_simulation:
        assert type(hip_simulation) in (float,int)
        todo_rawhlt.append('hip_simulation,%f' % float(hip_simulation))

    if hip_mitigation:
        assert hip_simulation
        todo_reco  .append('hip_mitigation')
        todo_ntuple.append('hip_mitigation')

    todo2s = ('RAWHLT', todo_rawhlt), ('RECO', todo_reco), ('NTUPLE', todo_ntuple)
    for todo2_name, todo2 in todo2s:
        if todo2:
            todo2 = ' '.join('todo=%s' % x for x in todo2)
            steering.append('TODO%s="%s"' % (todo2_name, todo2))

            if not fixed_salt:
                salt += ' ' + todo2

    salt = salt.replace(' ', '_').replace('=','EQ')
    steering.append('SALT="%s"' % salt)

    open(steering_fn, 'wt').write('\n'.join(steering) + '\n')

    if condor:
        cs = CondorSubmitter(batch_name = os.path.basename(config.General.workArea),
                             meat = dedent('''
                                           ./nstep.sh $((job+1)) 2>&1
                                           meatexit=$?
                                           mv FrameworkJobReport.xml ${workdir}/fjr_${job}.xml
                                           '''),
                             pset_template_fn = config.JobType.psetName,
                             input_files = ['nstep.sh'] + config.JobType.inputFiles,
                             stageout_files = config.JobType.outputFiles,
                             publish_name = config.Data.outputDatasetTag,
                             jdl_extras = 'request_memory = 3000',
                             )
        sample = MCSample(config.General.requestName,
                          '/%s/None/None' % config.General.requestName,
                          config.Data.totalUnits,
                          filenames = ['dummy'],
                          split_by = 'events',
                          events_per = config.Data.unitsPerJob
                          )
        cs.submit(sample)

    else:
        if not testing:
            try:
                output = crab_command('submit', config=config)
            except CRABConfigException:
                output = 'problem'
            open(os.path.join(config.General.workArea, 'crab_%s' % config.General.requestName, 'cs_ex'), 'wt').write(gitstatus_dir)
            print colors.boldwhite(name)
            pprint(output)
            print
        else:
            print 'crab config:'
            print config
            print 'steering.sh:'
            os.system('cat ' + steering_fn)
    os.remove(steering_fn)

####

metamap = {
    'neu': ('mfv_neu', 'mfv_neutralino'),
    'glu': ('mfv_glu', 'mfv_gluino'),
    'neuuds': ('mfv_neuuds', 'neutralino_uds'),
    'neuudb': ('mfv_neuudb', 'neutralino_udb'),
    'neutds': ('mfv_neutds', 'neutralino_tds'),
    'neutbb': ('mfv_neutbb', 'neutralino_tbb'),
    'neuubb': ('mfv_neuubb', 'neutralino_ubb'),
    'neucds': ('mfv_neucds', 'neutralino_cds'),
    'neucdb': ('mfv_neucdb', 'neutralino_cdb'),
    'neuudmu': ('mfv_neuudmu', 'neutralino_udmu'),
    'neuude': ('mfv_neuude', 'neutralino_ude'),
    'neuudtau': ('mfv_neuudtau', 'neutralino_udtau'),
    'ddbar': ('mfv_ddbar', 'gluino_ddbar'),
    'ccbar': ('mfv_ccbar', 'gluino_ccbar'),
    'bbbar': ('mfv_bbbar', 'gluino_bbbar'),
    'lq2': ('mfv_lq2', 'leptoquark'),
    'xxddbar': ('mfv_xxddbar', 'xxddbar'),
    'stopdbardbar': ('mfv_stopdbardbar', 'stop_dbardbar'),
    'stopbbarbbar': ('mfv_stopbbarbbar', 'stop_bbarbbar'),
}

if meta == 'scan':
    for _ in scanpack:
        submit(config, scanpack.batch_name, scanpack)

elif meta == 'ttbar':
    from modify import DummyBeamSpots
    todo2s = ['nominal'] + [x for x in dir(DummyBeamSpots) if not x.startswith('_')]
    for todo2 in todo2s:
        name = 'ttbar_%s' % todo2
        todo = 'ttbar'
        if todo2 != 'nominal':
            todo2 = 'weakmode,' + todo2
        else:
            todo2 = None
        submit(config, name, todo,
               todo_rawhlt=(todo2,),
               todo_reco  =(todo2,),
               todo_ntuple=(todo2,))

elif meta == 'minbias':
    name = meta
    todo = 'minbias'
    submit(config, name, todo)

elif meta.startswith('qcdht2000_gensim'):
    name = meta
    todo = 'qcdht2000'
    submit(config, name, todo)

elif meta.startswith('qcdht'):
    name = meta
    todo = meta.replace('qcdht', 'qcdht,')
    submit(config, name, todo)

elif meta.startswith('mugun'):
    name = meta
    todo = meta.replace('mugun', 'mugun,')
    submit(config, name, todo)

elif meta in metamap:
    def signal_point_iterator():
        if tau_masses:
            for tm in tau_masses:
                yield tm
        else:
            for tau in taus:
                for mass in masses:
                    tm = tau, mass
                    if tm in already:
                        continue
                    yield tm

    name_prefix, todo_fcn = metamap[meta]
    for tau, mass in signal_point_iterator():
        name = '%s_tau%06ium_M%04i' % (name_prefix, tau, mass)
        todo = '%s,%.1f,%i' % (todo_fcn, tau/1000., mass)
        submit(config, name, todo)

else:
    raise ValueError('invalid meta %r' % meta)


if not testing:
    for x in to_rm:
        os.remove(x)
