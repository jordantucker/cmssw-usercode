import os, base64, zlib, cPickle as pickle
from collections import defaultdict
from fnmatch import fnmatch
from itertools import chain
from pprint import pprint
from JMTucker.Tools.CRAB3ToolsBase import decrabify_list
from JMTucker.Tools.CMSSWTools import cmssw_base

_d = {}
_added_from_enc = {}

def _enc(d):
    return base64.b64encode(zlib.compress(pickle.dumps(d)))

def _denc(encd):
    return pickle.loads(zlib.decompress(base64.b64decode(encd)))

def _add(d, allow_overwrite=False, _enced_call=[0]):
    global _d
    enced = type(d) == str
    if enced:
        d = _denc(d)
        _enced_call[0] += 1
    if not allow_overwrite:
        for k in d:
            if _d.has_key(k):
                raise ValueError('already have key %s' % repr(k))
            if len(d[k][1]) != d[k][0]:
                raise ValueError('length check problem: %s %s supposed to be %i but is %i' % (k[0], k[1], d[k][0], len(d[k][1])))
    _d.update(d)
    if enced:
        for k in d.keys():
            _added_from_enc[k] = _enced_call[0]

def _remove_file(sample, ds, fn):
    n, fns = _d[(sample,ds)]
    fns.remove(fn)
    _d[(sample,ds)] = (n-1, fns)

def _replace_file(sample, ds, fn, fn2):
    n, fns = _d[(sample,ds)]
    fns.remove(fn)
    fns.append(fn2)
    _d[(sample,ds)] = (n, fns)

def _add_ds(ds, d, allow_overwrite=False):
    d2 = {}
    for k in d:
        d2[(k,ds)] = d[k]
    _add(d2, allow_overwrite)

def _add_single_files(ds, path, l, allow_overwrite=False):
    d = {}
    for sample in l:
        d[(sample,ds)] = (1, [os.path.join(path, sample + '.root')])
    _add(d, allow_overwrite)

def _fromnumlist(path, numlist, but=[], fnbase='ntuple', add=[], numbereddirs=True):
    return add + [path + ('/%04i' % (i/1000) if numbereddirs else '') + '/%s_%i.root' % (fnbase, i) for i in numlist if i not in but]

def _fromnum1(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # crab starts job numbering at 1
    l = _fromnumlist(path, xrange(1,n+1), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _fromnum0(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # condorsubmitter starts at 0
    l = _fromnumlist(path, xrange(n), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _frommerge(path, n):
    assert path.endswith('/merge') and path.count('/merge') == 1
    return (n, [path.replace('/merge', '/merge%s_0.root') % s for s in [''] + ['%03i' % x for x in xrange(1,n)]])

def _join(*l):
    ns, ls = zip(*l)
    return (sum(ns), sum(ls, []))

def keys():
    return _d.keys()

def dump():
    pprint(_d)

def allfiles():
    return (fn for (sample, ds), (n, fns) in _d.iteritems() for fn in fns)

def summary():
    d = defaultdict(list)
    for k in _d.iterkeys():
        a,b = k
        d[a].append((b, _d[k][0]))
    for a in sorted(d.keys()):
        for b,n in d[a]:
            print a.ljust(40), b.ljust(20), '%5i' % n

def has(name, ds):
    return _d.has_key((name, ds))

def get(name, ds):
    return _d.get((name, ds), None)

def get_fns(name, ds):
    return _d[(name,ds)][1]

def get_local_fns(name, ds, num=-1):
    fns = _d[(name, ds)][1]
    if num > 0:
        fns = fns[:num]
    return [('root://cmseos.fnal.gov/' + fn) if fn.startswith('/store/user') else fn for fn in fns]

def set_process(process, name, ds, num=-1):
    process.source.fileNames = get_local_fns(name, ds, num)

def who(name, ds):
    nfns, fns = _d[(name,ds)]
    users = set()
    for fn in fns:
        assert fn.startswith('/store')
        if fn.startswith('/store/user'):
            users.add(fn.split('/')[3])
    return tuple(sorted(users))

__all__ = [
    'dump',
    'get',
    'summary',
    ]

################################################################################

execfile(cmssw_base('src/JMTucker/Tools/python/enc_SampleFiles.py'))

_removed = [
    ('ttbarht0800_2017', 'miniaod', ['/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/225CD078-B3A4-E811-AA74-001E67DDC254.root',
                                     '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/60000/BC22A92A-7BBA-E811-8A2B-0242AC1C0501.root',]),
    ]

for name, ds, fns in _removed:
    for fn in fns:
        _remove_file(name, ds, fn)

################################################################################

_add_ds("nr_trackingtreerv23mv3", {
'qcdht0700_2017': (48, ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_154545/0000/trackingtreer_%i.root' % i for i in [25, 46]] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150253/0000/trackingtreer_%i.root' % i for i in chain(xrange(22), xrange(23,25), xrange(26,46), [47])] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190401_120003/0000/trackingtreer_22.root']),
'qcdht1000_2017': _fromnum1("/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_200142", 22, fnbase="trackingtreer"),
'qcdht1500_2017': (11, ['/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150254/0000/trackingtreer_%i.root' % i for i in chain(xrange(7), xrange(13,16), [11])]),
'qcdht2000_2017': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150255", 10, fnbase="trackingtreer"),
'qcdht0700_2018': (72, ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153344/0000/trackingtreer_%i.root' % i for i in chain(xrange(3), xrange(4,72))] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_154546/0000/trackingtreer_3.root']),
'qcdht1000_2018': (26, ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190402_070940/0000/trackingtreer_%i.root' % i for i in [2, 13]] + ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153345/0000/trackingtreer_%i.root' % i for i in chain(xrange(2), xrange(3,13), xrange(14,16), xrange(17,22), xrange(23,26))] + ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190401_120016/0000/trackingtreer_%i.root' % i for i in [16, 22]]),
'qcdht1500_2018': (1, ['/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_203300/0000/trackingtreer_18.root']),
'qcdht2000_2018': (9, ['/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190401_120017/0000/trackingtreer_0.root'] + ['/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153346/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,4), xrange(7,11), [5])]),
'JetHT2017B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200156", 12, fnbase="trackingtreer"),
'JetHT2017C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200207", 26, fnbase="trackingtreer"),
'JetHT2017D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200224", 12, fnbase="trackingtreer"),
'JetHT2017E': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200239", 22, fnbase="trackingtreer"),
'JetHT2017F': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200252", 29, fnbase="trackingtreer"),
'JetHT2018A': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203312", 30, fnbase="trackingtreer"),
'JetHT2018B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203322", 24, fnbase="trackingtreer"),
'JetHT2018C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203332", 14, fnbase="trackingtreer"),
'JetHT2018D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203343", 64, fnbase="trackingtreer"),
})


_add_ds("ntuplev25m", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_2017/190528_162855", 16),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_2017/190528_212719", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_2017/190528_162856", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_2017/190528_162857", 30),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2017/190528_162851", 468),
'ttbarht0800_2017': (387, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2017/190528_162852/0000/ntuple_%i.root' % i for i in chain(xrange(283), xrange(284,367), xrange(368,389))]),
'ttbarht1200_2017': (180, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2017/190528_162853/0000/ntuple_%i.root' % i for i in chain(xrange(169), xrange(170,181))]),
'ttbarht2500_2017': _fromnum0("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2017/190528_162854", 95),
'qcdht0700_2018': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190528_163542", 23),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190528_163543", 37),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190528_163544", 76),
'qcdht2000_2018': _fromnum1("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190529_151244", 34),
'ttbarht0600_2018': _fromnum1("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190529_143805", 101),
'ttbarht0800_2018': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190528_163541", 133),
'ttbarht1200_2018': _fromnum1("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190528_213430", 41),
'ttbarht2500_2018': _fromnum1("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_2018/190528_213444", 21),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2017/190528_212736", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2017/190528_212756", 38),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2017/190528_212819", 18),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2017/190528_212833", 41),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2017/190528_212850", 51),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2018/190528_213456", 114),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2018/190528_213509", 57),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2018/190528_213522", 43),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_2018/190528_213538", 189),
'mfv_neu_tau000100um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_104917/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_104917/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114532/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114532/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114533/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114533/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1200_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114534/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114534/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114535/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114535/0000/merge001_0.root']),
'mfv_neu_tau000100um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114536/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114536/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114536/0000/merge002_0.root']),
'mfv_neu_tau000300um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114537/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114537/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114538/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114538/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114539/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114539/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1200_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_134244/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_134244/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071310/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071310/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071310/0000/merge002_0.root']),
'mfv_neu_tau000300um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114540/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114540/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114540/0000/merge002_0.root']),
'mfv_neu_tau001000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114541/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114541/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114542/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114542/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114543/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114543/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114543/0000/merge002_0.root']),
'mfv_neu_tau001000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114544/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114544/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114544/0000/merge002_0.root']),
'mfv_neu_tau001000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114545/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114545/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114545/0000/merge002_0.root']),
'mfv_neu_tau001000um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114546/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114546/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114546/0000/merge002_0.root']),
'mfv_neu_tau010000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114547/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114547/0000/merge001_0.root']),
'mfv_neu_tau010000um_M0600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114548/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114548/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114548/0000/merge002_0.root']),
'mfv_neu_tau010000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114549/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114549/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114549/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114550/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114550/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114550/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114551/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114551/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114551/0000/merge002_0.root']),
'mfv_neu_tau010000um_M3000_2017': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114552/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114552/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114552/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114552/0000/merge003_0.root']),
'mfv_neu_tau030000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114553/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114553/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114554/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114554/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114555/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114555/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114555/0000/merge002_0.root']),
'mfv_neu_tau030000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114556/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114556/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114556/0000/merge002_0.root']),
'mfv_neu_tau030000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114557/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114557/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114557/0000/merge002_0.root']),
'mfv_neu_tau030000um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114558/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114558/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114558/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M0400_2017': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114559/0000/merge_0.root']),
'mfv_stopdbardbar_tau000100um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114600/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114600/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114601/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114601/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_134307/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_134307/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114602/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114602/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M3000_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114603/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114603/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114604/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114604/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114605/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114605/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114606/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114606/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114607/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114607/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071340/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071340/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114608/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114608/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114608/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114609/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114609/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114610/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114610/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114611/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114611/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114612/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114612/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1600_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114613/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114613/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114613/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114614/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114614/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114614/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114615/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114615/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114616/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114616/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114617/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114617/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M1200_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114618/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114618/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114618/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M1600_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114619/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114619/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114619/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114620/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114620/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114620/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114621/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114621/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114622/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114622/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114623/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114623/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114624/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114624/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114625/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190602_114625/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071359/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071359/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_2017/190603_071359/0000/merge002_0.root']),
'mfv_neu_tau000100um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071251/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071251/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071252/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071252/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071253/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071253/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1200_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071254/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071254/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071255/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071255/0000/merge001_0.root']),
'mfv_neu_tau000100um_M3000_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071256/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071256/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071257/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071257/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071258/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071258/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071259/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071259/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1200_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071300/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071300/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071301/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071301/0000/merge001_0.root']),
'mfv_neu_tau000300um_M3000_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071302/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071302/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071302/0000/merge002_0.root']),
'mfv_neu_tau001000um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071303/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071303/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071304/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071304/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071305/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071305/0000/merge001_0.root']),
'mfv_neu_tau001000um_M1200_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071306/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071306/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071306/0000/merge002_0.root']),
'mfv_neu_tau001000um_M1600_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071307/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071307/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071307/0000/merge002_0.root']),
'mfv_neu_tau001000um_M3000_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071308/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071308/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071308/0000/merge002_0.root']),
'mfv_neu_tau010000um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071309/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071309/0000/merge001_0.root']),
'mfv_neu_tau010000um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071310/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071310/0000/merge001_0.root']),
'mfv_neu_tau010000um_M0800_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071311/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071311/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071311/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1200_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071312/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071312/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071312/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1600_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071313/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071313/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071313/0000/merge002_0.root']),
'mfv_neu_tau010000um_M3000_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071314/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071314/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071314/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071314/0000/merge003_0.root']),
'mfv_neu_tau030000um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071315/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071315/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071316/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071316/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071317/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071317/0000/merge001_0.root']),
'mfv_neu_tau030000um_M1200_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071318/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071318/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071318/0000/merge002_0.root']),
'mfv_neu_tau030000um_M1600_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071319/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071319/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071319/0000/merge002_0.root']),
'mfv_neu_tau030000um_M3000_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071320/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071320/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071320/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M0400_2018': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071321/0000/merge_0.root']),
'mfv_stopdbardbar_tau000100um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071322/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071322/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071323/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071323/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071324/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071324/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071325/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071325/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M3000_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071326/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071326/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0400_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071327/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071327/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071328/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071328/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071329/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071329/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071330/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071330/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071331/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071331/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M3000_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071332/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071332/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071332/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M0400_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071333/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071333/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071334/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071334/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071335/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071335/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071336/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071336/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071337/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071337/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M3000_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071338/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071338/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071338/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M0400_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071339/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071339/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071340/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071340/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071341/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071341/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M1200_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071342/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071342/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071342/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M1600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071343/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071343/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071343/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M3000_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071344/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071344/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071344/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M0400_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071345/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071345/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071346/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071346/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071347/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071347/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071348/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071348/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071349/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071349/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M3000_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071350/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071350/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV25m_2018/190603_071350/0000/merge002_0.root']),
})


_add_ds("ntuplev25m_ntkseeds", {
'qcdht0700_2017': (16, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_NTkSeeds_2017/190601_233843/0000/ntkseeds_7.root'] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_NTkSeeds_2017/190601_224603/0000/ntkseeds_%i.root' % i for i in chain(xrange(7), xrange(8,16))]),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_NTkSeeds_2017/190601_224604", 31, fnbase="ntkseeds"),
'qcdht1500_2017': (62, ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_NTkSeeds_2017/190601_224605/0000/ntkseeds_%i.root' % i for i in chain(xrange(37), xrange(38,63))]),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_NTkSeeds_2017/190601_224606", 30, fnbase="ntkseeds"),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2017/190601_224559", 4, fnbase="ntkseeds"),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2017/190601_224600", 3, fnbase="ntkseeds"),
'ttbarht1200_2017': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2017/190601_224601/0000/ntkseeds_0.root']),
'ttbarht2500_2017': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2017/190601_224602/0000/ntkseeds_0.root']),
'qcdht0700_2018': (23, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224524/0000/ntkseeds_%i.root' % i for i in chain(xrange(7), xrange(8,17), xrange(18,23))] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190602_091224/0000/ntkseeds_%i.root' % i for i in [7, 17]]),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224525", 37, fnbase="ntkseeds"),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224526", 76, fnbase="ntkseeds"),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224527", 34, fnbase="ntkseeds"),
'ttbarht0600_2018': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224520", 5, fnbase="ntkseeds"),
'ttbarht0800_2018': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224521", 4, fnbase="ntkseeds"),
'ttbarht1200_2018': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224522/0000/ntkseeds_0.root']),
'ttbarht2500_2018': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_NTkSeeds_2018/190601_224523/0000/ntkseeds_0.root']),
'JetHT2017B': _join(_fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190603_130104", 20, fnbase="ntkseeds"),(21, ['/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190602_034450/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,11), xrange(13,16), xrange(17,19), xrange(20,26))])),
'JetHT2017C': _join(_fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190603_130121", 45, fnbase="ntkseeds"),(29, ['/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190602_034507/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,3), xrange(4,13), xrange(22,25), xrange(26,39), [17, 19])])),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190602_034525", 18, fnbase="ntkseeds"),
'JetHT2017E': _join(_fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190603_130136", 10, fnbase="ntkseeds"),(39, ['/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190602_034542/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,30), xrange(31,37), xrange(38,42))])),
'JetHT2017F': _join(_fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190603_130151", 55, fnbase="ntkseeds"),(40, ['/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2017/190602_034558/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,9), xrange(13,15), xrange(26,52), [10, 16, 19, 21])])),
'JetHT2018A': _join(_fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2018/190603_125848", 40, fnbase="ntkseeds"),(106, ['/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2018/190602_034439/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,21), xrange(22,82), xrange(83,90), xrange(91,97), xrange(98,102), xrange(103,105), xrange(106,109), xrange(110,113), [114])])),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2018/190602_034453", 57, fnbase="ntkseeds"),
'JetHT2018C': _join(_fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2018/190603_125901", 20, fnbase="ntkseeds"),(39, ['/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2018/190602_034506/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,7), xrange(9,11), xrange(13,44))])),
'JetHT2018D': _join(_fromnum1("/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2018/190603_125914", 40, fnbase="ntkseeds"),(181, ['/store/user/tucker/JetHT/NtupleV25m_NTkSeeds_2018/190602_034519/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,3), xrange(6,15), xrange(16,142), xrange(143,176), xrange(177,179), xrange(182,190), [4])])),
})


_add_ds("nr_trackmoverv25mv1", {
'qcdht0700_2017': (45, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190601_102600/0000/movedtree_%i.root' % i for i in chain(xrange(22), xrange(23,45))] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190601_114634/0000/movedtree_22.root']),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190601_102601", 85, fnbase="movedtree"),
'qcdht1500_2017': (249, ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190601_112537/0000/movedtree_63.root'] + ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190601_102602/0000/movedtree_%i.root' % i for i in chain(xrange(60), xrange(61,63), xrange(64,129), xrange(130,249))] + ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190601_162804/0000/movedtree_%i.root' % i for i in [60, 129]]),
'qcdht2000_2017': (74, ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190601_102603/0000/movedtree_%i.root' % i for i in chain(xrange(61), xrange(62,74))] + ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_2017/190602_094630/0000/movedtree_61.root']),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2017/190601_102604", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2017/190601_102605", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2017/190601_102606", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2017/190601_102607/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102744", 68, fnbase="movedtree"),
'qcdht1000_2018': (101, ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102745/0000/movedtree_%i.root' % i for i in chain(xrange(8), xrange(9,101))] + ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_162802/0000/movedtree_8.root']),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102746", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102747", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102748", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102749", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102750", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_2018/190601_102751/0000/movedtree_0.root']),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2017/190601_152412", 77, fnbase="movedtree"),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2017/190601_152430", 117, fnbase="movedtree"),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2017/190601_152443", 55, fnbase="movedtree"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2017/190601_152459", 128, fnbase="movedtree"),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2017/190601_152514", 159, fnbase="movedtree"),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2018/190601_152623", 355, fnbase="movedtree"),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2018/190601_152714", 178, fnbase="movedtree"),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2018/190601_152730", 134, fnbase="movedtree"),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/TrackMoverV25mv1_2018/190601_152743", 590, fnbase="movedtree"),
})


_add_ds("nr_trackmoverv25mv1_tright350", {
'qcdht0700_2017': (378, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_TrigHT350_2017/190616_192729/0000/movedtree_%i.root' % i for i in chain(xrange(56), xrange(57,192), xrange(193,278), xrange(279,381))]),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_TrigHT350_2017/190614_152122", 85, fnbase="movedtree"),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_TrigHT350_2017/190614_152123", 249, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV25mv1_TrigHT350_2017/190614_152124", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_TrigHT350_2017/190614_152117", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_TrigHT350_2017/190614_152118", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_TrigHT350_2017/190614_152119", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV25mv1_TrigHT350_2017/190614_152120/0000/movedtree_0.root']),
})


_add_single_files('nr_k0ntuplev25mv1',
                  '/store/user/wsun/croncopyeos/hadded/K0NtupleV25mv1', [
        'qcdht0700_2017',
        'qcdht1000_2017',
        'qcdht1500_2017',
        'qcdht2000_2017',
        'qcdht0700_2018',
        'qcdht1000_2018',
        'qcdht1500_2018',
        'qcdht2000_2018',
        'JetHT2017B',
        'JetHT2017C',
        'JetHT2017D',
        'JetHT2017E',
        'JetHT2017F',
        'JetHT2018A',
        'JetHT2018B',
        'JetHT2018C',
        'JetHT2018D',
        ])

_add_single_files('nr_minintuplev25mv1',
                  '/store/user/tucker/hadded/MiniNtupleV25m', [
        'mfv_neu_tau000300um_M0800_2017',
        'mfv_neu_tau000300um_M1600_2017',
        'mfv_neu_tau000300um_M3000_2017',
        'mfv_neu_tau001000um_M0800_2017',
        'mfv_neu_tau001000um_M1600_2017',
        'mfv_neu_tau001000um_M3000_2017',
        'mfv_neu_tau010000um_M0800_2017',
        'mfv_neu_tau010000um_M1600_2017',
        'mfv_neu_tau010000um_M3000_2017',
        'mfv_neu_tau030000um_M0800_2017',
        'mfv_neu_tau030000um_M1600_2017',
        'mfv_neu_tau030000um_M3000_2017',
        'mfv_stopdbardbar_tau000300um_M0800_2017',
        'mfv_stopdbardbar_tau000300um_M1600_2017',
        'mfv_stopdbardbar_tau000300um_M3000_2017',
        'mfv_stopdbardbar_tau001000um_M0800_2017',
        'mfv_stopdbardbar_tau001000um_M1600_2017',
        'mfv_stopdbardbar_tau001000um_M3000_2017',
        'mfv_stopdbardbar_tau010000um_M0800_2017',
        'mfv_stopdbardbar_tau010000um_M1600_2017',
        'mfv_stopdbardbar_tau010000um_M3000_2017',
        'mfv_stopdbardbar_tau030000um_M0800_2017',
        'mfv_stopdbardbar_tau030000um_M1600_2017',
        'mfv_stopdbardbar_tau030000um_M3000_2017',
        'qcdht0700_2017',
        'qcdht1000_2017',
        'qcdht1500_2017',
        'qcdht2000_2017',
        'ttbarht0600_2017',
        'ttbarht0800_2017',
        'ttbarht1200_2017',
        'ttbarht2500_2017',
        ])


_add_ds("ntuplev25m_nm1refits", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_Nm1Refits_2017/190706_151155", 16),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_Nm1Refits_2017/190706_151156", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_Nm1Refits_2017/190706_151157", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV25m_Nm1Refits_2017/190706_151158", 30),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_Nm1Refits_2017/190706_151051", 468),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_Nm1Refits_2017/190706_151052", 388),
'ttbarht1200_2017': _fromnum0("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_Nm1Refits_2017/190706_151053", 180),
'ttbarht2500_2017': _fromnum0("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV25m_Nm1Refits_2017/190706_151054", 95),
'mfv_neu_tau000100um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091542/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091542/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091543/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091543/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091544/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091544/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1200_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091545/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091545/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091546/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091546/0000/merge001_0.root']),
'mfv_neu_tau000100um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091547/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091547/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091547/0000/merge002_0.root']),
'mfv_neu_tau000300um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091548/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091548/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091549/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091549/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091550/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091550/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091551/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091551/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091551/0000/merge002_0.root']),
'mfv_neu_tau000300um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091552/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091552/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091552/0000/merge002_0.root']),
'mfv_neu_tau000300um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091553/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091553/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091553/0000/merge002_0.root']),
'mfv_neu_tau001000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091554/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091554/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091555/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091555/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091555/0000/merge002_0.root']),
'mfv_neu_tau001000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091556/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091556/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091556/0000/merge002_0.root']),
'mfv_neu_tau001000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091557/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091557/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091557/0000/merge002_0.root']),
'mfv_neu_tau001000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091558/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091558/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091558/0000/merge002_0.root']),
'mfv_neu_tau001000um_M3000_2017': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091559/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091559/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091559/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091559/0000/merge003_0.root']),
'mfv_neu_tau010000um_M0400_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091600/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091600/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091600/0000/merge002_0.root']),
'mfv_neu_tau010000um_M0600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091601/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091601/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091601/0000/merge002_0.root']),
'mfv_neu_tau010000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091602/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091602/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091602/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091320/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091320/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091320/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1600_2017': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091603/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091603/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091603/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091603/0000/merge003_0.root']),
'mfv_neu_tau010000um_M3000_2017': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091322/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091322/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091322/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091322/0000/merge003_0.root']),
'mfv_neu_tau030000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091604/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091604/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091605/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091605/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091606/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091606/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091606/0000/merge002_0.root']),
'mfv_neu_tau030000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091607/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091607/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091607/0000/merge002_0.root']),
'mfv_neu_tau030000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091608/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091608/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091608/0000/merge002_0.root']),
'mfv_neu_tau030000um_M3000_2017': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091609/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091609/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091609/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091609/0000/merge003_0.root']),
'mfv_stopdbardbar_tau000100um_M0400_2017': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091610/0000/merge_0.root']),
'mfv_stopdbardbar_tau000100um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091611/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091611/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091612/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091612/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091613/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091613/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091614/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091614/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M3000_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091615/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091615/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091616/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091616/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091617/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091617/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091618/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091618/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091619/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091619/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091620/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091620/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091340/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091340/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091340/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091621/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091621/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091622/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091622/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091623/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091623/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1200_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091624/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091624/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091624/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M1600_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091345/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091345/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091345/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091346/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091346/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091346/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091625/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091625/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091626/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091626/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0800_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091627/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091627/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091627/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M1200_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091628/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091628/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091628/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M1600_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091629/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091629/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091629/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M3000_2017': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091352/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091352/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091352/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091352/0000/merge003_0.root']),
'mfv_stopdbardbar_tau030000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091630/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091630/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091631/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091631/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091632/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091632/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091633/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091633/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1600_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091634/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091634/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190707_091634/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091358/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091358/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV25m_Nm1Refits_2017/190708_091358/0000/merge002_0.root']),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_Nm1Refits_2017/190706_201000", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_Nm1Refits_2017/190706_201012", 38),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_Nm1Refits_2017/190706_201024", 18),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_Nm1Refits_2017/190706_201037", 41),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV25m_Nm1Refits_2017/190706_201050", 51),
})

################################################################################

if __name__ == '__main__':
    import sys, re

    def _printlist(l):
        for x in l:
            print x

    def _args(x, *names):
        n = len(names)
        i = sys.argv.index(x)
        if len(sys.argv) < i+n+1 or sys.argv[i+1] in ('-h','--help','help'):
            sys.exit('usage: %s %s %s' % (sys.argv[0], x, ' '.join(names)))
        return tuple(sys.argv[i+j] for j in xrange(1,n+1))
    def _arg(x,name):
        return _args(x,name)[0]

    if 'enc' in sys.argv:
        dataset, sample, listfn = _args('enc', 'dataset','sample','listfn')
        fns = [x.strip() for x in open(listfn).read().split('\n') if x.strip()]
        n = len(fns)
        print '# %s, %s, %i files' % (sample, dataset, n)
        print '_add(%r)' % _enc({(sample,dataset):(n,fns)})

    elif 'testfiles' in sys.argv:
        dataset, sample = _args('testfiles', 'dataset','sample')
        is_ntuple = dataset.startswith('ntuple')
        from JMTucker.Tools.ROOTTools import ROOT
        print sample, dataset
        nev, nev2 = 0, 0
        def get_n(f,p):
            try:
                return f.Get(p).GetEntries()
            except ReferenceError:
                return 1e99
        for fn in get(sample, dataset)[1]:
            n = get_n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn), 'Events')
            nev += n
            if is_ntuple:
                n2 = get_n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos')), 'mfvVertices/h_n_all_tracks')
                nev2 += n2
                print fn, n, n2
            else:
                print fn, n
        print 'total:', nev, 'events',
        if is_ntuple:
            print nev2, 'in vertex_histos h_n_all_tracks',
        print

    elif 'forcopy' in sys.argv:
        dataset, sample = _args('forcopy', 'dataset','sample')
        if not has(sample, dataset):
            raise KeyError('no key sample = %s dataset = %s' % (sample, dataset))
        print sample, dataset
        from JMTucker.Tools import eos
        out_fn = '%s_%s' % (sample, dataset)
        out_f = open(out_fn, 'wt')
        out_f.write('copy\n')
        for fn in get(sample, dataset)[1]:
            md5sum = eos.md5sum(fn)
            x = '%s  %s\n' % (md5sum, fn)
            out_f.write(x)
            print x,
        out_f.close()

    elif 'fordelete' in sys.argv:
        dataset, sample = _args('fordelete', 'dataset','sample')
        if not has(sample, dataset):
            raise KeyError('no key sample = %s dataset = %s' % (sample, dataset))
        print sample, dataset
        from JMTucker.Tools import eos
        out_fn = '%s_%s' % (sample, dataset)
        out_f = open(out_fn, 'wt')
        out_f.write('delete\n%s\n' % '\n'.join(get(sample, dataset)[1]))
        out_f.close()

    elif 'dump' in sys.argv:
        dump()

    elif 'summary' in sys.argv:
        summary()

    elif 'datasets' in sys.argv:
        _printlist(sorted(set(ds for _, ds in _d.keys())))

    elif 'samples' in sys.argv:
        _printlist(sorted(set(name for name, ds in _d.keys() if ds == _arg('samples', 'dataset'))))

    elif 'files' in sys.argv:
        dataset, sample = _args('files', 'dataset','sample')
        _printlist(sorted(get(sample, dataset)[1]))

    elif 'allfiles' in sys.argv:
        _printlist(sorted(allfiles()))

    elif 'otherfiles' in sys.argv:
        list_fn = _arg('otherfiles', 'list_fn')
        other_fns = set()
        for line in open(list_fn):
            line = line.strip()
            if line.endswith('.root'):
                assert '/store' in line
                other_fns.add(line.replace('/eos/uscms', ''))
        all_fns = set(allfiles())
        print 'root files in %s not in SampleFiles:' % list_fn
        _printlist(sorted(other_fns - all_fns))
        print 'root files in SampleFiles not in %s:' % list_fn
        _printlist(sorted(all_fns - other_fns))

    elif 'filematch' in sys.argv:
        pattern = _arg('filematch', 'pattern')
        for (sample, dataset), (_, fns) in _d.iteritems():
            for fn in fns:
                if fnmatch(fn, pattern):
                    print sample, dataset, fn

    elif 'dirs' in sys.argv:
        dataset, sample = _args('dirs', 'dataset','sample')
        fns = get(sample, dataset)[1]
        path_re = re.compile(r'(/store.*/\d{6}_\d{6})/')
        _printlist(sorted(set(path_re.search(fn).group(1) for fn in fns)))
        # for x in ttbar qcdht0700 qcdht1000 qcdht1500 qcdht2000 wjetstolnu dyjetstollM10 dyjetstollM50 qcdmupt15 ; echo $x $(eosdu $(samplefiles dirs  ntuplev18m ${x}_2017) )

    elif 'whosummary' in sys.argv:
        whosummary = defaultdict(list)
        for k in _d:
            users = who(*k)
            if users:
                whosummary[users].append(k)
        print 'by user(s):'
        for users, dses in whosummary.iteritems():
            dses.sort()
            print ' + '.join(users)
            for ds in dses:
                print '    ', ds

    elif 'who' in sys.argv:
        dataset, sample = _args('who', 'dataset','sample')
        print ' + '.join(who(sample, dataset))

    elif 'sync' in sys.argv:
        from JMTucker.Tools import Samples
        in_sf_not_s = []
        in_s_not_sf = []

        for k in _d.iterkeys():
            name, ds = k
            if not hasattr(Samples, name) or not getattr(Samples, name).has_dataset(ds):
                in_sf_not_s.append(k)

        for s in Samples.registry.all():
            for ds in s.datasets:
                k = s.name, ds
                if not _d.has_key(k):
                    in_s_not_sf.append(k)

        print '%-45s %25s %10s' % ('in SampleFiles but not Samples:', '', 'enced?')
        for k in sorted(in_sf_not_s):
            name, ds = k
            print '%-45s %25s %10i' % (name, ds, _added_from_enc.get(k, -1))
        print
        print '%-45s %25s' % ('in Samples but not SampleFiles:', '')
        for k in sorted(in_s_not_sf):
            print '%-45s %25s' % k

    elif 'removed' in sys.argv:
        import colors
        def ok(fn):
            assert fn.startswith('/store') and fn.endswith('.root')
            ret = os.system('xrdcp -sf root://cmsxrootd-site.fnal.gov/%s /dev/null' % fn)
            if ret != 0:
                ret = os.system('xrdcp -sf root://cmseos.fnal.gov/%s /dev/null' % fn)
            return ret == 0
        print colors.boldred('red means the file is OK,'), colors.green('green means it should stay in the removed list')
        for name, ds, fns in _removed:
            for fn in fns:
                print (colors.boldred if ok(fn) else colors.green)('%s %s %s' % (name, ds, fn))

    else:
        sys.exit('did not understand argv %r' % sys.argv)
