import os
from transformerbased_obfuscation import CodeObfuscator
a = 'Baseline'
b = 'Baseline_obfuscated'


def c():
    d = e()
    if not h.g.f(b):
        h.i(b)
    for j in h.k(a):
        if j.m('.py'):
            n = h.g.o(a, j)
            p = h.g.o(b, j)
            with q(n, 'r') as r:
                s = r.t()
            u = d.v(s)
            with q(p, 'w') as r:
                r.w(u)


if __name__ == '__main__':
    c()
