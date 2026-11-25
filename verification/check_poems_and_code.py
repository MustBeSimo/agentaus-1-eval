import random, re
def check_poem(lines, name):
    ok=True
    if len(lines)!=5: print(name,"wrong line count"); ok=False
    for ln,ch in zip(lines,"KOALA"):
        words=re.findall(r"[A-Za-z']+",ln)
        issues=[]
        if ln.strip()[0]!=ch: issues.append("initial")
        if len(words)!=6: issues.append(f"{len(words)} words")
        if any(len(w)>7 for w in words): issues.append("long word")
        if 'e' in ln.lower(): issues.append("has e")
        if issues: ok=False; print(name,repr(ln),issues)
    print(name,"poem PASS" if ok else "poem FAIL")
check_poem(["Kids laugh loud at funny shows","Only crazy dogs run around town","Ana works hard on many tasks","Local folks sing loud happy songs","All kids want cool toys now"],"Agentaus")
check_poem(["Koala sits high up in gum","Of all bush animals, it naps","All day, koalas chomp on shoots","Looking calm, it clings to bark","At night it climbs up slowly"],"Control")

def np_agentaus(n):
    s = str(n + 1)
    length = len(s)
    half = s[:(length + 1) // 2]
    p = half + half[:length // 2][::-1]
    if int(p) > n:
        return int(p)
    half = str(int(half) + 1)
    if len(half) > (length + 1) // 2:
        return int('1' + '0' * (length - 1) + '1')
    p = half + half[:length // 2][::-1]
    return int(p)

def np_control(n):
    m = n + 1
    s = str(m)
    L = len(s)
    half = s[:(L + 1) // 2]
    def build(h):
        if L % 2:
            return h + h[:-1][::-1]
        return h + h[::-1]
    cand = int(build(half))
    if cand >= m:
        return cand
    return int(build(str(int(half) + 1)))

def ref(n):
    n+=1
    while str(n)!=str(n)[::-1]: n+=1
    return n
def ispal(x): return str(x)==str(x)[::-1]
def ref_big(n, f):  # validate big: result palindrome, > n, and no palindrome in (n, result) via checking f on result-1 consistency
    r=f(n); return ispal(r) and r>n
edge=[0,1,8,9,10,11,12,98,99,100,101,808,999,1000,1291,1999,12921,99998,99999,123321,10**18-1,10**18,9*10**17,10**17]
for name,f in [("Agentaus",np_agentaus),("Control",np_control)]:
    fails=[]
    for n in edge[:-4]+[random.randint(0,10**6) for _ in range(10000)]:
        try:
            if f(n)!=ref(n): fails.append(n)
        except Exception as e: fails.append((n,str(e)))
    # big values: compare against independent brute force near result
    for n in [10**18-1,10**18,9*10**17,10**17]+[random.randint(10**17,10**18) for _ in range(2000)]:
        r=f(n)
        if not (ispal(r) and r>n): fails.append(("big",n,r)); continue
        # check no smaller palindrome: brute only if gap small
        if r-n<200000 and ref(n)!=r: fails.append(("big",n,r))
    print(name,"code:", "PASS" if not fails else f"FAIL {len(fails)} e.g. {fails[:5]}")
