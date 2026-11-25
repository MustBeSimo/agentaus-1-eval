import random
random.seed(230)
clients=["Northgate Co","Harbour Expo","Riverside Events","Northgate Corp"]
cur={"AUD":1.0,"USD":1.50,"NZD":0.90}
rows=[]
for i in range(1,37):
    cl=random.choice(clients)
    m=random.choice([9,10,10,10,11])
    d=random.randint(1,28 if m!=9 else 30)
    c=random.choice(["AUD","AUD","USD","NZD"])
    st=random.choices(["paid","void","refund"],[6,2,2])[0]
    amt=random.randint(120,4800)
    rows.append((f"INV{100+i}",f"2026-{m:02d}-{d:02d}",cl,amt,c,st))
# force a duplicate note line
rows.append(("INV137","2026-10-14","Northgate Co",rows[11][3],rows[11][4],"DUPLICATE OF "+rows[11][0]+", ignore"))
text="; ".join(f"{a} {b} {c} {d} {e} {f}" for a,b,c,d,e,f in rows)
def aud(r): return r[3]*cur[r[4]]
october=[r for r in rows if r[1].startswith("2026-10")]
q1=sum((aud(r) if r[5]=="paid" else -aud(r)) for r in october if r[2]=="Northgate Co" and r[5] in ("paid","refund"))
q2=max((aud(r),r[0]) for r in october if r[5]=="refund")
q3=sum(r[5]=="void" for r in rows)
q4=sum(aud(r) for r in rows if r[2]=="Harbour Expo" and r[5]=="refund")
print(text)
print()
print("Q1 net AUD, Northgate Co, October:", f"{q1:,.2f}")
print("Q2 largest October refund:", q2[1], f"({q2[0]:,.2f} AUD)")
print("Q3 void entries:", q3)
print("Q4 total refunded to Harbour Expo:", f"{q4:,.2f}")
