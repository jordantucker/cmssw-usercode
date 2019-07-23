from JMTucker.Tools.ROOTTools import *
from statmodel import ebins
ROOT.TH1.AddDirectory(0)

do_bquark = False
is_mc = True
only_10pc = False
year = '2017p8'
version = 'V25m'
set_style()
ps = plot_saver(plot_dir('closure_%s%s%s_%s' % (version.capitalize(), '' if is_mc else '_data', '_10pc' if only_10pc else '', year)), size=(700,700), root=False, log=False)

fns = ['2v_from_jets%s_%s_3track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '2v_from_jets%s_%s_7track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '2v_from_jets%s_%s_4track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '2v_from_jets%s_%s_5track_default_%s.root' % ('' if is_mc else '_data', year, version)
       ]

# for overlaying the btag-based template
fns_btag = ['2v_from_jets%s_%s_3track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version), 
            '2v_from_jets%s_%s_7track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version), 
            '2v_from_jets%s_%s_4track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version), 
            '2v_from_jets%s_%s_5track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version)
            ]

ntk = []
for fn in fns:
    for x in fn.split('_'):
        if 'track' in x:
            ntk.append(int(x[:1]))

def errprop(val0, val1, err0, err1):
    if val0 == 0 and val1 == 0:
        return 0
    elif val1 == 0:
        return err0 / val0
    elif val0 == 0:
        return err1 / val1
    else:
        return ((err0 / val0)**2 + (err1 / val1)**2)**0.5

def scale_and_draw_template(template, i, simulated, color) :
    template.SetStats(0)
    template.SetLineColor(color)
    template.SetLineWidth(2)
    if simulated.Integral() > 0:
        newerrarray = []
        simerr = ROOT.Double(0)
        sim = simulated.IntegralAndError(0, simulated.GetNbinsX(), simerr)
        for bin in range(template.GetNbinsX() + 1):
            newerr = template.GetBinContent(bin) / template.Integral() * simerr
            newerrarray.append(newerr)
        template.Scale(sim/template.Integral())
        for bin, err in enumerate(newerrarray):
            template.SetBinError(bin, err)
    else:
        template.Scale(1./template.Integral())
    template.Draw('hist sames')

def make_closure_plots(i):
    dvv_closure = ('h_2v_dvv', 'h_c1v_dvv')
    dphi_closure = ('h_2v_absdphivv', 'h_c1v_absdphivv')

    for closure in (dvv_closure, dphi_closure):
        simulated = ROOT.TFile(fns[i]).Get(closure[0])
        simulated.SetTitle(';|#Delta#phi_{VV}|;Events' if 'phi' in closure[0] else ';d_{VV} (cm);Events')
        simulated.SetStats(0)
        simulated.SetLineColor(ROOT.kBlue)
        simulated.SetLineWidth(2)
        simulated.SetMinimum(0)
        simulated.Draw()

        template_btag = ROOT.TFile(fns_btag[i]).Get(closure[1])
        scale_and_draw_template(template_btag, i, simulated, ROOT.kRed)

        uncertband_btag = template_btag.Clone('uncertband_btag')
        uncertband_btag.SetFillColor(ROOT.kRed-3)
        uncertband_btag.SetFillStyle(3004)
        uncertband_btag.Draw('E2 sames')

        l1 = ROOT.TLegend(0.35, 0.75, 0.85, 0.85)
        l1.AddEntry(simulated, 'Simulated events' if is_mc else 'Data')
        l1.AddEntry(template_btag, 'Background template' + (' (btag method)' if do_bquark else ''))

        if do_bquark:
            template = ROOT.TFile(fns[i]).Get(closure[1])
            scale_and_draw_template(template, i, simulated, ROOT.kGreen+2)

            uncertband = template.Clone('uncertband')
            uncertband.SetFillColor(ROOT.kGreen-3)
            uncertband.SetFillStyle(3005)
            uncertband.Draw('E2 sames')
            l1.AddEntry(template, 'Background template (bquark method)')


        l1.SetFillColor(0)
        l1.Draw()
        ps.save('%s-track' % ntk[i] if 'phi' not in closure[0] else '%s_dphi' % ntk[i])

def calculate_ratio(x, y, xerr, yerr):
    y_ = y
    yerr_ = yerr

    if y == 0: 
        y_ = 1.
        yerr_ = 1.

    r = x/y_
    e = r * errprop(x, y_, xerr, yerr_)
    return r, e

def get_bin_integral_and_stat_uncert(hist):
    sample = 'MCeffective' if is_mc else 'data100pc'
    if not is_mc and only_10pc:
        sample = 'data10pc'
    ebin = ebins['%s_%s_%dtrack' % (sample, year, 4 if ntracks==7 else ntracks)]

    bin1 = bin1_err = bin2 = bin2_err = bin3 = bin3_err = 0.

    if 'c1v' not in hist.GetName():
        bin1, bin1_err = get_integral(hist, xhi=0.04, include_last_bin=False)
        bin2, bin2_err = get_integral(hist, xlo=0.04, xhi=0.07, include_last_bin=False)
        bin3, bin3_err = get_integral(hist, xlo=0.07, xhi=0.4, include_last_bin=False)
    else:
        bin1 = get_integral(hist, 0., 0.04, integral_only=True, include_last_bin=False)
        bin1_err = bin1 * ebin[0]
        bin2 = get_integral(hist, 0.04, 0.07, integral_only=True, include_last_bin=False)
        bin2_err = bin2 * ebin[1]
        bin3 = get_integral(hist, 0.07, 0.4, integral_only=True, include_last_bin=False)
        bin3_err = bin3 * ebin[2]
    return [(bin1, bin1_err), (bin2, bin2_err), (bin3, bin3_err)]

def get_norm_frac_uncert(bins, total):
    allbins = []
    norm_sum = 0.
    for bin in bins:
        norm_sum += (bin[1] / total)**2

    for bin in bins:
        frac_uncert = ((1 - bin[0] / total) * (bin[1] / total)**2 + (bin[0] / total)**2 * norm_sum)**0.5
        allbins.append((bin[0] / total, frac_uncert))
    return allbins

def get_ratios(nums, dens):
    ratios = []
    for num, den in zip(nums, dens):
        r_bin, r_bin_err = calculate_ratio(num[0], den[0], num[1], den[1])
        ratios.append((r_bin, r_bin_err))
    return ratios

for i, ntracks in enumerate(ntk):
    make_closure_plots(i)

    simulated = ROOT.TFile(fns[i]).Get('h_2v_dvv')
    constructed = ROOT.TFile(fns_btag[i]).Get('h_c1v_dvv')

    if simulated.Integral() > 0:
        constructed.Scale(simulated.Integral()/constructed.Integral())
    else:
        constructed.Scale(1./constructed.Integral())

    sim_total, sim_total_err = get_integral(simulated)
    sim_bins = get_bin_integral_and_stat_uncert(simulated)

    con_total, con_total_err = get_integral(constructed)
    con_bins = get_bin_integral_and_stat_uncert(constructed)

    sim_bin_norm = get_norm_frac_uncert(sim_bins, sim_total)
    con_bin_norm = get_norm_frac_uncert(con_bins, con_total)

    ratios = get_ratios(con_bin_norm, sim_bin_norm)

    sim = (sim_total, sim_total_err) + tuple(x for bin in sim_bins for x in bin)
    con = (con_total, con_total_err) + tuple(x for bin in con_bins for x in bin)
    sim_norm = tuple(x for bin in sim_bin_norm for x in bin)
    con_norm = tuple(x for bin in con_bin_norm for x in bin)
    rat = tuple(x for bin in ratios for x in bin)

    print '%s-track' % ntk[i]
    print '  two-vertex events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % sim
    print ' constructed events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % con
    print '     dVV normalized:                    0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % sim_norm
    print '    dVVC normalized:                    0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % con_norm
    print '   ratio dVVC / dVV:                    0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % rat
