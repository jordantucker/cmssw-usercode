#!/usr/bin/env python

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
def a(f0,f1,cb,cbbar):
    return e(f0,f1)**2 * c(cb,cbbar) * n(f0)
def f2(f0,f1,cb,cbbar):
    return a(f0,f1,cb,cbbar)/(1+a(f0,f1,cb,cbbar))


def print_f2(ntk,f0,f1,cb,cbbar):
    print 'ntk = %d: f0 = %.2f, f1 = %.2f, cb/cbbar = %.3f/%.3f = %.2f, nb/nbbar = %.2f, effb/effbbar = %.1f, f2 = %.2f' % (ntk, f0, f1, cb, cbbar, c(cb,cbbar), n(f0), e(f0,f1), f2(f0,f1,cb,cbbar))

if __name__ == '__main__':
    print_f2(3, 0.17, 0.46, 0.588, 0.551)
    print_f2(4, 0.17, 0.49, 0.567, 0.520)
    print_f2(5, 0.17, 0.55, 0.539, 0.494)