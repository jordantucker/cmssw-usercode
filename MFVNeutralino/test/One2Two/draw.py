#!/usr/bin/env python

import sys, os
from JMTucker.Tools.general import typed_from_argv
input_fn = [x for x in sys.argv if x.endswith('_histos.root') and os.path.isfile(x)][0]
ntracks = typed_from_argv(int)
if ntracks is None:
    ntracks = 5

from array import array
from math import pi
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetOptStat(2222222)
ROOT.gStyle.SetOptFit(2222)
ps = plot_saver('plots/one2two/ntracks%i_%s' % (ntracks, input_fn.replace('_histos.root', '')), size=(600,600))

f = ROOT.TFile(input_fn)

def get_h(name):
    ex = ''
    if ntracks != 5:
        ex = 'Ntracks%i' % ntracks
    return f.Get('mfvOne2Two%s/%s' % (ex, name))

####

for name in 'h_1v_xy h_2v_xy'.split():
    h = get_h(name)
    h.SetTitle(';vertex x (cm);vertex y (cm)')
    h.SetStats(0)
    if '1v' in name:
        h.Draw('colz')
    else:
        h.SetMarkerStyle(20)
        h.SetMarkerSize(1.3)
        h.Draw('scat same')
        ps.save(name, logz=True)

for name in 'h_2v_bs2ddist h_2v_bs2ddist_0 h_2v_bs2ddist_1 h_1v_bs2ddist'.split():
    h = get_h(name)
    h.Rebin(2)
    h.SetTitle(';vertex xy distance to beamspot (cm);vertices/20 #mum')
    h.Draw()
    ps.save(name)

for name in 'h_2v_bsdz h_2v_bsdz_0 h_2v_bsdz_1 h_1v_bsdz'.split():
    h = get_h(name)
    h.Rebin(2)
    h.SetTitle(';vertex #Delta z to beamspot (cm);vertices/0.4 cm')
    h.Draw()
    ps.save(name)

for name in 'h_2v_bs2ddist_v_bsdz h_2v_bs2ddist_v_bsdz_0 h_2v_bs2ddist_v_bsdz_1 h_1v_bs2ddist_v_bsdz'.split():
    h = get_h(name)
    h.SetTitle(';vertex #Delta z to beamspot (cm);vertex xy distance to beamspot (cm)')
    h.SetStats(0)
    h.Draw('colz')
    ps.save(name, logz=True)

h = get_h('h_2v_svdz')
h.Fit('gaus', 'ILQ')
ps.save('h_2v_svdz')

for name in 'h_1v_svdz h_1v_svdz_all'.split():
    h = get_h(name)
    h.SetTitle(';vertex #Delta z (cm);events/100 #mum')
    h.Draw()
    ps.save(name)

for name in 'h_2v_svdz_v_dphi h_1v_svdz_v_dphi'.split():
    h = get_h(name)
    h.SetTitle(';vertex #Delta #phi;vertex #Delta z (cm)')
    h.SetStats(0)
    h.Draw('colz')
    ps.save(name, logz=True)

for name in 'h_2v_ntracks h_1v_ntracks h_2v_ntracks01 h_1v_ntracks01'.split():
    h = get_h(name)
    if '01' in name:
        h.SetTitle(';sum of ntracks 0 and 1;events')
        h.Draw()
    else:
        h.SetTitle(';ntracks 0;ntracks 1')
        h.Draw('colz')
    ps.save(name)

####

h2v = get_h('h_2v_dphi')
h1v = get_h('h_1v_dphi')
hfn = get_h('h_fcn_dphi')

h1v.SetLineColor(ROOT.kRed)
hfn.SetLineColor(ROOT.kGreen+2)

h1v.Scale(h2v.Integral()/h1v.Integral())
hfn.Scale(h2v.Integral()/hfn.Integral())

h2v.SetTitle(';#Delta#phi;events/0.63')
h2v.Draw()
h1v.Draw('sames')
hfn.Draw('sames')
ps.c.Update()
differentiate_stat_box(h2v, (1,0), new_size=(0.25, 0.25))
differentiate_stat_box(h1v, (1,1), new_size=(0.25, 0.25))
differentiate_stat_box(hfn, (1,2), new_size=(0.25, 0.25))
ps.save('deltaphi')

####

h2v_lt35 = get_h('h_2v_lt35_dphi')
h2v_gt35 = get_h('h_2v_lt35_dphi')

h2v_gt35.SetLineColor(ROOT.kRed)

h2v_lt35.Draw()
h2v_gt35.Draw('sames')
ps.c.Update()
differentiate_stat_box(h2v_gt35)
ps.save('deltaphi_ltgt35')

####

h2v = get_h('h_2v_svdz')
h1v = get_h('h_1v_svdz')
hfn = get_h('h_fcn_dz')

h1v.SetLineColor(ROOT.kRed)
hfn.SetLineColor(ROOT.kGreen+2)

h1v.Scale(h2v.Integral()/h1v.Integral())
hfn.Scale(h2v.Integral()/hfn.Integral())

h2v.SetTitle(';#Delta z;events/0.02 cm')
h2v.Draw()
h1v.Draw('sames')
hfn.Draw('sames')
ps.c.Update()
differentiate_stat_box(h2v, (1,0), new_size=(0.25, 0.25))
differentiate_stat_box(h1v, (1,1), new_size=(0.25, 0.25))
differentiate_stat_box(hfn, (1,2), new_size=(0.25, 0.25))
ps.save('dz')

####

def svdist2d_comp(norm_below, shift=None, rebin=None, save=True):
    name = ('norm%.3f' % norm_below).replace('.','p')
    if shift is not None:
        name += '_shift%i' % shift
    
    h2v = get_h('h_2v_svdist2d').Clone('h2v')
    h1v = get_h('h_1v_svdist2d').Clone('h1v')

    if rebin is not None:
        h2v.Rebin(rebin)
        h1v.Rebin(rebin)

    h1v.Scale(1/h1v.Integral())
    nbins = h1v.GetNbinsX()

    if shift is not None:
        h1v_vals = [h1v.GetBinContent(i+1) for i in xrange(nbins)]
        h1v_vals_new = []
        for i in xrange(nbins):
            ifrom = i - shift
            h1v_vals_new.append(h1v_vals[ifrom] if ifrom >= 0 else 0.)

        h1v = ROOT.TH1F('h1v_shift%i' % shift, '', nbins, h1v.GetXaxis().GetXmin(), h1v.GetXaxis().GetXmax())
        for i in xrange(nbins):
            h1v.SetBinContent(i+1, h1v_vals_new[i])
            h1v.SetBinError(i+1, 0)
        #print 'shift', shift, 'mean', h1v.GetMean()

    ksdist = h1v.KolmogorovTest(h2v, 'M')
    ksprob = h1v.KolmogorovTest(h2v)
    ks = (ksdist, ksprob)

    h2v.SetLineWidth(2)
    h1v.SetLineColor(ROOT.kRed)

    h1v.Scale(h2v.Integral(1, h2v.FindBin(norm_below))/h1v.Integral(1, h1v.FindBin(norm_below)))

    h2v.SetTitle('norm_below %f shift %i;xy distance between vertex 0 and 1 (cm);events/40 #mum' % (norm_below, shift))

    h2v.Draw('e')
    h1v.Draw('sames')
    ps.c.Update()
    differentiate_stat_box(h2v, 0, new_size=(0.3, 0.3))
    differentiate_stat_box(h1v,    new_size=(0.3, 0.3))
    if save:
        ps.save('svdist2d_%s' % name)

    for opt in ('ge', 'le'):
        ch2v = cumulative_histogram(h2v, opt)
        ch1v = cumulative_histogram(h1v, opt)

        ch2v.SetTitle(';x = svdist2d (cm);# events w/ svdist2d #%sq x' % opt)
        ch2v.SetStats(0)
        ch1v.SetStats(0)
        ch2v.SetLineWidth(2)
        ch1v.SetLineColor(ROOT.kRed)
        ch2v.Draw()
        ch1v.Draw('hist same')
        if save:
            ps.save('svdist2d_%s_cumul%s' % (name, opt))

    return ks

for norm_below in (1, 0.024, 0.048):
    svdist2d_comp(norm_below, 0)

n = 30
shifts = range(n)
kses = [svdist2d_comp(1, shift, save=False) for shift in shifts]
min_ksdist = 1e99
best_shift = None
for i, (ksdist, ksprob) in enumerate(kses):
    if ksdist < min_ksdist:
        min_ksdist = ksdist
        best_shift = shifts[i]

shifts = array('d', shifts)
for i,name in enumerate(('dist', 'prob')):
    g = ROOT.TGraph(n, shifts, array('d', [x[i] for x in kses]))
    g.SetTitle(';shift;KS %s' % name)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(1)
    g.Draw('ALP')
    ps.save('KS_%s_v_shift' % name)

for norm_below in (1, 0.024, 0.048):
    svdist2d_comp(norm_below, best_shift)

####

if 1:
    verbose = 'Q'
    h = get_h('h_2v_dphi')

    for i in xrange(2, 17, 2):
        if verbose == 'V':
            print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
        fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
        res = h.Fit(fcn, 'IRS' + verbose)
        ps.save('power_%i' % i)
        #res.Print()

    h = get_h('h_2v_abs_dphi')

    for i in xrange(2, 17, 2):
        if verbose == 'V':
            print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
        fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
        res = h.Fit(fcn, 'IRS' + verbose)
        ps.save('abs_power_%i' % i)
        #res.Print()
