from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)
set_style()

ps = plot_saver(plot_dir('pileup_efficiency_run2_v15'), size=(600,600), pdf=True)

bins = to_array([0,10,13,15,65])
nbins = len(bins)-1

hists = [
    ('presel', 'mfvEventHistosPreSel'),
    ('onevtx', 'mfvEventHistosOnlyOneVtx'),
    ('twovtx', 'mfvEventHistosFullSel'),
    ('sigreg', 'mfvEventHistosSigReg')
    ]

xxx = [
    (3, '/uscms_data/d2/tucker/crab_dirs/HistosV15/background.root', 'Ntk3'),
    (4, '/uscms_data/d2/tucker/crab_dirs/HistosV15/background.root', 'Ntk4'),
    (5, '/uscms_data/d2/tucker/crab_dirs/HistosV15/background.root', ''),
]

for ntk, fn, s2 in xxx:
    print fn, ntk
    f = ROOT.TFile(fn)
    def geth(s,s2):
        if s.endswith('PreSel'):
            n = s + '/h_npu'
        else:
            n = s2 + s + '/h_npu'
        print n
        return f.Get(n)
    #hs = [(n, geth(s).Rebin(nbins, n, bins)) for n,s in hists]
    hs = [(n, geth(s,s2).Clone(n)) for n,s in hists]

    for n, h in hs:
        h.Rebin(5)
        exec n+'=h'
        if n != 'presel':
            g = histogram_divide(h, presel, use_effective=True)
            g.SetTitle('%s-track %s;true nPU;efficiency' % (ntk,n))
            g.Draw('AP')
            fcn = ROOT.TF1('fcn', 'pol1', 10, 50)
            g.Fit(fcn, 'QR')
            g.GetYaxis().SetRangeUser(0, fcn.GetParameter(0)*5)
            if fcn.GetParameter(0) > 0:
                print n, fcn.GetParameter(1) / fcn.GetParameter(0) * 4
        else:
            h.Draw()
        h.GetXaxis().SetRangeUser(0,70)
        if ntk == 4 and n == 'onevtx':
            h.GetYaxis().SetRangeUser(0,0.005)
        ps.save(n + '_ntk%i' % ntk, log=False)
