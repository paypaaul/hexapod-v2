import os
import re
md=open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'schemi.md')).read()
def analyse(sec_net, sec_wire, wire_re, alias):
    nets={}
    for line in sec_net.splitlines():
        m=re.match(r'\| (\w+) \| (.*?) \| ',line)
        if not m or m.group(1)=='Rete': continue
        nets[m.group(1)]=set(re.findall(r'\b([A-U]-\d{1,2})\b',m.group(2)))
    par={}
    def f(x):
        par.setdefault(x,x)
        while par[x]!=x: x=par[x]
        return x
    def u(a,b): par[f(a)]=f(b)
    edges=[(a,b,'ponte') for a,b in re.findall(r'([A-U]-\d{1,2})–([A-U]-\d{1,2})',sec_wire)]
    edges+=[(a,b,'filo '+n) for n,a,b,r in re.findall(wire_re,sec_wire)]
    for a,b,c in re.findall(r'([A-U]-\d{1,2})–([A-U]-\d{1,2})–([A-U]-\d{1,2})',sec_wire): edges.append((b,c,'ponte'))
    for a,b,_ in edges: u(a,b)
    h2n={}
    for n,hs in nets.items():
        for hh in hs:
            if hh in h2n and h2n[hh]!=n: print('FORO IN DUE RETI',hh,h2n[hh],n)
            h2n[hh]=n
    for a,b,k in edges:
        na,nb=alias.get(h2n.get(a),h2n.get(a)),alias.get(h2n.get(b),h2n.get(b))
        if na!=nb: print('ARCO FRA RETI',k,a,b,na,nb)
    for n,hs in nets.items():
        g={}
        for x in hs: g.setdefault(f(x),[]).append(x)
        if len(g)>1: print('RETE NON CONNESSA',n,list(g.values()))
b=md.split('### 1.2')[1].split('### 1.3')[0]; w=md.split('### 1.3')[1].split('### 1.4')[0]
print('== basetta'); analyse(b,w,r'\| (\d+) \| ([A-U]-\d+) \| ([A-U]-\d+) \| (\w+) \|',{'3V3_ESP':'3V3S','J1':'3V3S'})
b2=md.split('### 2.2')[1].split('### 2.3')[0]; w2=md.split('### 2.3')[1].split('### 2.4')[0]
print('== scheda'); analyse(b2,w2,r'\| (\d+) \| ([A-G]-\d+) \| ([A-G]-\d+) \| (\w+) \|',{})
