import os
import sys, ast, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fili_b
B = fili_b.B
def valuta(o):
    R, fail = fili_b.instrada_ordine(o)
    tot = sum(len(f['perc']) for f in B.fili if f['perc'])
    return 1000 * len(fail) + 5 * len(R.incroci()) + 2 * len(R.paralleli()) + tot, len(fail), len(R.incroci()), len(R.paralleli()), tot
best_o = ast.literal_eval(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ordine_b.txt')).read())
best = valuta(best_o)
print('inizio', best)
rnd = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
t = time.time()
for it in range(int(sys.argv[1])):
    o = best_o[:]
    for _ in range(rnd.randint(1, 4)):
        a, b = rnd.randrange(len(o)), rnd.randrange(len(o))
        o.insert(b, o.pop(a))
    v = valuta(o)
    if v[0] <= best[0]:
        if v[0] < best[0]: print(it, v)
        best, best_o = v, o
print('fine', best, time.time() - t)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ordine_b.txt'), 'w').write(repr(best_o))
