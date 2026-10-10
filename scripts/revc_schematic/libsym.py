import sexp, functools
LIB='/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/'
EXTRA = {}   # library name -> path of a project-local .kicad_sym
@functools.lru_cache(None)
def lib(name): return sexp.parse(open(EXTRA.get(name, LIB + name + '.kicad_sym')).read())
def raw(libname,sym):
    for s in sexp.find(lib(libname),'symbol'):
        if s[1]==sym: return s
    raise KeyError(sym)
def flat(libname,sym):
    """return flattened symbol node (list) with name sym"""
    s=raw(libname,sym); ext=sexp.get(s,'extends')
    if not ext: return s
    p=flat(libname,ext[1])
    props={c[1]:c for c in sexp.find(s,'property')}
    out=[]
    for c in p:
        if isinstance(c,list) and c and c[0]=='property' and c[1] in props: out.append(props.pop(c[1]))
        elif isinstance(c,list) and c and c[0]=='symbol':
            out.append(['symbol',c[1].replace(ext[1],sym,1)]+c[2:])
        else: out.append(c)
    out[1]=sym
    # insert remaining child props after last property
    idx=max(i for i,c in enumerate(out) if isinstance(c,list) and c and c[0]=='property')
    for v in props.values(): idx+=1; out.insert(idx,v)
    return out
def pins(node):
    r=[]
    for u in sexp.find(node,'symbol'):
        unit=int(u[1].split('_')[-2])
        for p in sexp.find(u,'pin'):
            at=sexp.get(p,'at'); num=sexp.get(p,'number')[1]; nm=sexp.get(p,'name')[1]
            r.append(dict(unit=unit,num=num,name=nm,etype=p[1],x=float(at[1]),y=float(at[2]),a=float(at[3]),len=float(sexp.get(p,'length')[1])))
    return r
