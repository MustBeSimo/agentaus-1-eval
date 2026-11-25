import itertools, random
# A1 logic puzzle uniqueness
P=["Ana","Ben","Cal","Dee"]; R=["Designer","Engineer","Lawyer","Manager"]; C=["Perth","Hobart","Darwin","Cairns"]
sols=[]
for r in itertools.permutations(R):
  for c in itertools.permutations(C):
    role=dict(zip(P,r)); city=dict(zip(P,c)); inv_r={v:k for k,v in role.items()}; inv_c={v:k for k,v in city.items()}
    ok = role["Ana"]!="Engineer" and city["Ana"]!="Perth" and city[inv_r["Lawyer"]]=="Darwin" \
      and city["Ben"] in("Hobart","Cairns") and role["Dee"] in("Manager","Designer") \
      and city[inv_r["Engineer"]]=="Perth" and role["Cal"]!="Lawyer" and role[inv_c["Cairns"]]=="Designer" \
      and role["Ben"]!="Designer"
    if ok: sols.append((role,city))
print("A1 solutions:",len(sols)); [print(s) for s in sols]
# A4
def nd(n): return sum(1 for d in range(1,int(n**.5)+1) if n%d==0 for _ in ([0] if d*d==n else [0,0]))
print("A4:",sum(1 for n in range(1,2027) if nd(n)%2 and nd(n+1)%2))
# A5
cnt=0
for m in range(1<<15):
  s=[i+1 for i in range(15) if m>>i&1]
  if any(b-a==1 for a,b in zip(s,s[1:])): continue
  if sum(s)%3==0: cnt+=1
print("A5:",cnt)
