#!/usr/bin/env python
import pandas as pd

#f0 = the fraction of preselected events with b quarks
#nb    = the number of preselected events with b quarks
#nbbar = the number of preselected events without b quarks
#nb/nbbar = n(f0)
def n(f0):
    return f0/(1-f0)

#f1 = the fraction of one-vertex events with b quarks
#effb    = the efficiency to reconstruct a vertex in an event with b quarks
#effbbar = the efficiency to reconstruct a vertex in an event without b quarks
#effb/effbbar = e(f0,f1)
def e(f0,f1):
    return f1/(1-f1) * 1/n(f0)

#f2 = the fraction of two-vertex events with b quarks
#cb    = the integrated efficiency correction for dVVC constructed from one-vertex events with b quarks
#cbbar = the integrated efficiency correction for dVVC constructed from one-vertex events without b quarks
#cb/cbbar = c(cb,cbbar)
def c(cb,cbbar):
    return cb/cbbar
def a(f0,f1,cb,cbbar,s):
    return e(f0,f1)**2 * c(cb,cbbar) * n(f0) * 1./s**2
def f2(f0,f1,cb,cbbar,s):
    return a(f0,f1,cb,cbbar,s)/(1+a(f0,f1,cb,cbbar,s))


def print_f2(ntk,f0,f1,cb,cbbar,s):
    f2_val = f2(f0,f1,cb,cbbar,s)
    print 'ntk = %d: f0 = %.3f, f1 = %.3f, cb/cbbar = %.3f/%.3f = %.2f, nb/nbbar = %.2f, effb/effbbar = %.1f, f2 = %.2f' % (ntk, f0, f1, cb, cbbar, c(cb,cbbar), n(f0), e(f0,f1), f2_val)
    return f2_val


def fb(ft,efft,frt):
    return (ft-frt)/(efft-frt)

if __name__ == '__main__':

    effs = pd.read_csv('../MiniTree/efficiencies/all_effs.csv',index_col='variant')
    cb_vals = pd.read_csv('cb_vals/cb_vals.csv',index_col='variant')

    ntk_list = [3,4,5,7]

    for is_data in False, True :
        for sys_var in ['nom','bcjet_up','bcjet_down','ljet_up','ljet_down'] :
            for year in ['2017','2018','2017p8'] :
                f2_vals_printout = ''

                year_formatted = year
                if is_data :
                    year_formatted = "data_" + year_formatted

                print 'new: f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); %s; %s' % (year_formatted, sys_var)
        
                for ntk in ntk_list :

                    # ntk == 5 is blinded still!
                    if is_data :
                        if ntk == 5 or ntk == 7 : continue 

                    var_1v  = str(ntk) + 'trk_1v_%s_%s' % (year, sys_var)
                    ft_1v   = effs.at[var_1v,'ft']
                    efft_1v = effs.at[var_1v,'efft']
                    frt_1v  = effs.at[var_1v,'frt']

                    var_presel = 'presel_%s_%s' % (year, sys_var)
                    ft_presel   = effs.at[var_presel,'ft']
                    efft_presel = effs.at[var_presel,'efft']
                    frt_presel  = effs.at[var_presel,'frt']

                    cb_label = year_formatted+'_'+str(ntk)+'trk_'
                    cb    = cb_vals.at[cb_label+'cb','cb_val']
                    cbbar = cb_vals.at[cb_label+'cbbar','cb_val']

                    f2_val = print_f2(ntk, fb(ft_presel,efft_presel,frt_presel), fb(ft_1v,efft_1v,frt_1v), cb, cbbar, 1)
                    
                    if f2_vals_printout != '' :
                        f2_vals_printout += ', '
                    f2_vals_printout += "(%s,'%.3f,%.3f')" % (ntk, f2_val, 1-f2_val)

                print '###########################'
                print "For utilities.py (%s, %s):" % (year_formatted, sys_var)
                print f2_vals_printout
                print '###########################'
                print

