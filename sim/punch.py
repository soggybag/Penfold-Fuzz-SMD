"""Penfold v2 envelope shape: buffered ENV (a note that rises in ~2 ms and decays naturally, tau 0.8 s, 6 V peak) into the LM13700 Iabc pin
(~1.2 V) through SUSTAIN (R_s) and PUNCH (C_p -> node X with R_d to GND -> 1N4148 -> R_p). Prints Iabc vs time (uA)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ng import run
def net(rs, rp, cp=1e-6, rd=100e3):
    p = f"CP env x {cp}\nRD x 0 {rd}\nDP x y D1N4148\nRP y iabc {rp}\n" if rp else ""
    return f"""punch
.model D1N4148 D(Is=2.52n Rs=0.568 N=1.752 Cjo=4p)
BENV env 0 V=6*(1-exp(-time/0.0007))*exp(-time/0.8)
RS env iabc {rs}
{p}VI iabc 0 1.2
"""
T = (0.002, 0.01, 0.05, 0.1, 0.2, 0.4, 0.8, 1.5)
def curve(rs, rp, **k):
    cmds = ['tran 0.2m 1.6 0 0.2m'] + [f'meas tran i{n} find i(VI) at={t}' for n, t in enumerate(T)]
    out = run(net(rs, rp, **k).splitlines() + ['.end'], cmds)
    v = {}
    for l in out:
        l = l.replace('stdout ', '', 1).strip()
        if l.startswith('i') and '=' in l and l[1].isdigit():
            try: v[int(l.split()[0][1:])] = -float(l.split('=')[1].split()[0]) * 1e6
            except Exception: pass
    return [v.get(n, 0) for n in range(len(T))]
if __name__ == '__main__':
    print('time (s)            ' + ''.join(f'{t:>7}' for t in T))
    for lab, rs, rp, kw in (('v1.0 now (R15 220k)', 220e3, None, {}), ('sustain only 470k', 470e3, None, {}),
                            ('470k + punch 47k', 470e3, 47e3, {}), ('470k + punch 22k', 470e3, 22e3, {}),
                            ('470k + punch 47k, Rd 47k', 470e3, 47e3, {'rd': 47e3}), ('470k + punch 47k, Rd 330k', 470e3, 47e3, {'rd': 330e3})):
        print(f'{lab:26s}' + ''.join(f'{x:7.1f}' for x in curve(rs, rp, **kw)))
    print('Iabc in uA (VCA gain is proportional to Iabc)')
