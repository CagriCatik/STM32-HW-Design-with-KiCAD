import re
class Q(str): pass
def parse(s):
    tok=re.compile(r'\s*(?:(\()|(\))|("(?:[^"\\]|\\.)*")|([^\s()"]+))')
    st=[[]];i=0
    while i<len(s):
        m=tok.match(s,i)
        if not m or m.end()==i: break
        i=m.end()
        if m.group(1): st.append([])
        elif m.group(2): x=st.pop(); st[-1].append(x)
        elif m.group(3): st[-1].append(Q(m.group(3)[1:-1]))
        elif m.group(4): st[-1].append(m.group(4))
    return st[0][0]
def find(n,k): return [c for c in n if isinstance(c,list) and c and c[0]==k]
def get(n,k):
    r=find(n,k); return r[0] if r else None
def nets(path):
    t=parse(open(path).read()); out={}
    for net in find(get(t,'nets'),'net'):
        name=get(net,'name')[1]
        out[name]=sorted((get(nd,'ref')[1],get(nd,'pin')[1],(get(nd,'pinfunction') or [0,''])[1]) for nd in find(net,'node'))
    return out

def q(s): return '"'+str(s)+'"'  # Q holds raw (already escaped) text
def dump(n,ind=0):
    if isinstance(n,Q): return q(n)
    if not isinstance(n,list): return str(n)
    simple=all(not isinstance(c,list) for c in n)
    if simple: return '('+' '.join(dump(c) for c in n)+')'
    pad='\t'*(ind+1)
    return '('+dump(n[0])+''.join(('\n'+pad+dump(c,ind+1)) if isinstance(c,list) else ' '+dump(c) for c in n[1:])+'\n'+'\t'*ind+')'
