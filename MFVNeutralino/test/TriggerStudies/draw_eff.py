import sys, os
from array import array
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.Tools.Samples import *

version = 'v6'
zoom = False #(0.98,1.005)
save_more = True
data_only = False
use_qcd = False
num_dir = 'num900450ak'
year = 2016
which = typed_from_argv(int, 3)
data_period, int_lumi = [
    ('',  35861. if year == 2016 else 2689.),
    ('BthruG', 27255.),
    ('CthruG', 21472.),
    ('H', 8606.),
    ('B3', 5783.),
    ('C',  2573.),
    ('D',  4248.),
    ('E',  4009.),
    ('F',  3102.),
    ('G',  7540.),
    ('H2', 8391.),
    ('H3',  215.),
    ][which]

########################################################################

if any((year not in (2015, 2016),
        year == 2015 and which > 0,
        year == 2015 and num_dir == 'num900',
        num_dir == 'num800' and (data_period.startswith('H') or year == 2016 and data_period == ''))):
    raise ValueError('invalid combo: %s %s %s' % (num_dir, year, data_period))

root_dir = '/uscms_data/d2/tucker/crab_dirs/TrigEff%s' % version
plot_path = 'TrigEff%s_%s_%s%s' % (version, num_dir, year, data_period)
if zoom:
    plot_path += '_zoom'

set_style()
ROOT.gStyle.SetOptStat(0)
ps = plot_saver(plot_dir(plot_path), size=(600,600), log=False, pdf=True)
ROOT.TH1.AddDirectory(0)

data_fn = os.path.join(root_dir, 'SingleMuon%s%s.root' % (year, data_period))
data_f = ROOT.TFile(data_fn)

if data_only:
    bkg_samples, sig_samples = [], []
else:
    if year == 2015:
        bkg_samples = [ttbar_2015, wjetstolnusum_2015, dyjetstollM50sum_2015, dyjetstollM10sum_2015]
        sig_samples = [] #mfv_signal_samples_2015  no miniaod
    elif year == 2016:
        bkg_samples = [ttbar, wjetstolnu, dyjetstollM50, dyjetstollM10]
        sig_samples = [getattr(Samples, 'official_mfv_neu_tau01000um_M%04i' % m) for m in (300, 400, 800, 1200, 1600)] + [Samples.official_mfv_neu_tau10000um_M0800]
    if use_qcd:
        bkg_samples.append(qcdmupt15_2015 if year == 2015 else qcdmupt15)

n_bkg_samples = len(bkg_samples)
for sample in bkg_samples:
    sample.fn = os.path.join(root_dir, sample.name + '.root')
    sample.f = ROOT.TFile(sample.fn)

for sample in sig_samples:
    sample.fn = os.path.join(root_dir, sample.name + '.root')
    sample.f = ROOT.TFile(sample.fn)

kinds = ['']
ns = ['h_jet_ht']

def fit_limits(kind, n):
    if 'ht' in n:
        return 650, 5000
    else:
        if 'pf' in kind:
            if 'pt_4' in n:
                return 85, 250
            else:
                return 75, 250
        else:
            return 60, 250

def draw_limits(kind, n):
    if 'ht' in n:
        return 500, 5000
    else:
        if 'pf' in kind:
            if 'pt_4' in n:
                return 85, 250
            else:
                return 75, 250
        else:
            return 60, 250

def make_fcn(name, kind, n):
    fcn = ROOT.TF1(name, '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', *fit_limits(kind,n))
    fcn.SetParNames('floor', 'ceil', 'turnmu', 'turnsig')
    if 'ht' in n:
        fcn.SetParameters(0, 1, 900, 100)
    else:
        fcn.SetParameters(0, 1, 48, 5)
    fcn.SetParLimits(1, 0, 1)
    fcn.SetLineWidth(2)
    fcn.SetLineStyle(2)
    
    return fcn

def rebin_pt(h):
    a = to_array(range(0, 100, 5) + range(100, 150, 10) + [150, 180, 220, 260, 370, 500])
    return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)

def rebin_ht(h):
    a = to_array(range(0, 500, 20) + range(500, 1000, 50) + range(1000, 1500, 100) + range(1500, 2000, 250) + [2000, 3000, 5000])
    hnew = h.Rebin(len(a)-1, h.GetName() + '_rebin', a)
    move_overflow_into_last_bin(hnew)
    return hnew

def get(f, kind, n):
    def rebin(h):
        return h
    if 'pt' in n:
        rebin = rebin_pt
    elif 'ht' in n:
        rebin = rebin_ht
    return rebin(f.Get(kind + '%s/%s' % (num_dir, n))), rebin(f.Get(kind + 'den/%s' % n))

########################################################################

for kind in kinds:
    for n in ns:
        print
        print '============================================================================='
        print kind, n
        print '-----------------------'
        subname = '%s_%s' % (kind, n) if kind else n

        bkg_num, bkg_den = None, None
        sum_scaled_nums, sum_scaled_dens = 0., 0.
        sum_scaled_nums_var, sum_scaled_dens_var = 0., 0.

        reses = []
        for sample in bkg_samples:
            subsubname = subname + '_' + sample.name

            num, den = sample.num, sample.den = get(sample.f, kind, n)

            if save_more:
                den.Draw('hist text00')
                ps.save(subsubname + '_den',log=True)

            if den.Integral():
                rat = histogram_divide(num, den)
                rat.Draw('AP')
                if 'pt' in n:
                    rat.GetXaxis().SetLimits(0, 260)
                elif 'ht' in n:
                    rat.GetXaxis().SetLimits(0, draw_limits(kind,n)[1])

                fcn = make_fcn('f_' + subsubname, kind, n)
                res = rat.Fit(fcn, 'RQS')
                reses.append(res)
                if save_more:
                    ps.save(subsubname)
            else:
                reses.append(None)

            sample.total_events = -1
            scale = sample.partial_weight(sample.f) * int_lumi

            print '%s (%f)' % (sample.name, scale)
            ll = 1000. #limits(kind, n)[0]
            ib = num.FindBin(ll)
            ni = num.Integral(ib, 10000)
            di = den.Integral(ib, 10000)
            sum_scaled_nums += ni*scale
            sum_scaled_dens += di*scale
            sum_scaled_nums_var += scale**2 * ni
            sum_scaled_dens_var += scale**2 * di
            print '   %10i %10i %10.2f %10.2f  %.6f [%.6f, %.6f]' % ((ni, di, ni*scale, di*scale) + clopper_pearson(ni, di))
            #res.Print()

            num.Scale(scale)
            den.Scale(scale)
            if bkg_num is None and bkg_den is None:
                bkg_num = num.Clone('bkg_num')
                bkg_den = den.Clone('bkg_den')
            else:
                bkg_num.Add(num)
                bkg_den.Add(den)

        if reses:
            pars = [reses[0].GetParameterName(i) for i in xrange(reses[0].NPar())]
            for ipar, parname in enumerate(pars):
                subsubname = subname + '_' + parname
                hpar = ROOT.TH1F(parname, '', n_bkg_samples, 0, n_bkg_samples)
                for isam, sample in enumerate(bkg_samples):
                    #if sample.name == 'qcdmupt15' and 'Mu1' in kind:
                    #    continue
                    #print isam, reses[isam].Parameter(ipar), reses[isam].ParError(ipar)
                    hpar.SetBinContent(isam+1, reses[isam].Parameter(ipar))
                    hpar.SetBinError  (isam+1, reses[isam].ParError (ipar))
                    hpar.GetXaxis().SetBinLabel(isam+1, sample.name)
                hpar.Draw('hist e')
                hpar.SetLineWidth(2)
                fcnpar = ROOT.TF1('f_'  + subsubname, 'pol0')
                fcnpar.SetLineWidth(1)
                hpar.Fit(fcnpar, 'Q')
                ps.c.Update()
                move_stat_box(hpar, (0.507, 0.664, 0.864, 0.855))
                if parname == 'floor':
                    hpar.GetYaxis().SetRangeUser(0, 0.3)
                elif parname == 'ceil':
                    hpar.GetYaxis().SetRangeUser(0.2, 1)
                    move_stat_box(hpar, (0.143, 0.147, 0.5, 0.339))
                elif parname == 'turnmu':
                    hpar.GetYaxis().SetRangeUser(0, 1500)
                elif parname == 'turnsig':
                    hpar.GetYaxis().SetRangeUser(0, 300)
                ps.save(subsubname)

        if sum_scaled_dens_var > 0 and sum_scaled_dens > 0:
            bkg_effective_den = sum_scaled_dens**2 / sum_scaled_dens_var
            bkg_effective_num = sum_scaled_nums / sum_scaled_dens * bkg_effective_den
            print 'sum bkgs with effective n =', bkg_effective_den
            print '   %10.2f %10.2f %10s %10s  %.6f [%.6f, %.6f]' % ((sum_scaled_nums, sum_scaled_dens, '', '') + clopper_pearson(bkg_effective_num, bkg_effective_den))
            print '+- %10.2f %10.2f' % (sum_scaled_nums_var**0.5, sum_scaled_dens_var**0.5)

        if 'gen' in n:
            continue

        print 'data' #, data_num.GetEntries(), data_den.GetEntries()
        data_num, data_den = get(data_f, kind, n)
        ll = 1000. #limits(kind, n)[0]
        ib = data_num.FindBin(ll)
        ni = data_num.Integral(ib, 10000)
        di = data_den.Integral(ib, 10000)
        print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
        print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)
        if sum_scaled_nums and sum_scaled_dens:
            print 'data/mc:'
            print '   %10.4f %10.4f' % (ni/sum_scaled_nums, di/sum_scaled_dens)
            ivnum = clopper_pearson_poisson_means(ni, sum_scaled_nums)
            ivden = clopper_pearson_poisson_means(di, sum_scaled_dens)
            print '+- %10.4f %10.4f' % ((ivnum[2] - ivnum[1])/2, (ivden[2] - ivden[1])/2)

        data_rat = histogram_divide(data_num, data_den)
        bkg_rat = histogram_divide(bkg_num, bkg_den, use_effective=True) if bkg_num and bkg_den else None

        for r in (data_rat, bkg_rat):
            if not r:
                continue
            if 'pt' in n:
                r.GetXaxis().SetLimits(0, 260)
                i = int(n.split('_')[-1])
                k = 'PF' if 'pf' in kind else 'calo'
                r.SetTitle(';%ith %s jet p_{T} (GeV);efficiency' % (i, k))
            elif 'ht' in n:
                r.GetXaxis().SetLimits(0, draw_limits(kind, n)[1])
                k = ''
                r.SetTitle(';%s H_{T} (GeV);efficiency' % k)
            r.GetHistogram().SetMinimum(0)
            r.GetHistogram().SetMaximum(1.05)
            r.SetLineWidth(2)

        data_rat.Draw('AP')
        if zoom:
            data_rat.GetYaxis().SetRangeUser(*zoom)
        ROOT.gStyle.SetOptFit(1111)
        data_fcn = make_fcn('f_data', kind, n)
        data_fcn.SetLineColor(ROOT.kBlack)
        data_res = data_rat.Fit(data_fcn, 'RQS')
        print '\ndata:'
        data_res.Print()
        if bkg_rat:
            bkg_fcn = make_fcn('f_bkg', kind, n)
            bkg_fcn.SetLineColor(2)
            bkg_res = bkg_rat.Fit(bkg_fcn, 'RQS')
            print '\nbkg:'
            bkg_res.Print()

            bkg_rat.SetFillStyle(3001)
            bkg_rat.SetFillColor(2)
            bkg_rat.Draw('E2 same')

        ps.c.Update()
        move_stat_box(data_rat, 'inf' if zoom else (0.518, 0.133, 0.866, 0.343))
        if bkg_rat:
            s = move_stat_box(bkg_rat, 'inf' if zoom else (0.518, 0.350, 0.866, 0.560))
            s.SetLineColor(2)
            s.SetTextColor(2)

        ps.save(subname)

        print '\nsignals'
        for sample in sig_samples:
            sig_num, sig_den = get(sample.f, kind, n)
            ll = 1000. # fit_limits(kind, n)[0]
            ib = sig_num.FindBin(ll)
            ni = sig_num.Integral(ib, 10000)
            di = sig_den.Integral(ib, 10000)
            print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
            print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)
