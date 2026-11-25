"""Ground truth for the computable items in rounds 1 to 3."""
import datetime

print("R1.3  37*43 - 1591/37 =", 37 * 43 - 1591 / 37)
print("R1.5  1 Jan 2000 weekday:", datetime.date(2000, 1, 1).strftime("%A"))
print("R2.3  48271*69621 =", 48271 * 69621)


def dedupe(xs):
    seen = set()
    return [x for x in xs if x not in seen and not seen.add(x)]


print("R2.4  dedupe([3,1,3,2,1]) =", dedupe([3, 1, 3, 2, 1]))
print("R2.5  reversed:", "Trellis Data"[::-1], "| vowels:", sum(c in "aeiou" for c in "encyclopaedia"))
print("R2.7  day after 28 Feb 2029:", datetime.date(2029, 2, 28) + datetime.timedelta(days=1))
print("R3.1  digit sum 10 below 1000:", sum(1 for n in range(1, 1000) if sum(map(int, str(n))) == 10))
print("R3.2  x^2-7y^2=1, x<1000:", [(x, y) for x in range(1, 1000) for y in range(1, 400) if x * x - 7 * y * y == 1])
