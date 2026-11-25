from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)

OUT = "Agentaus_1_vs_Claude_test_report.pdf"

INK = colors.HexColor("#1f2328")
MUTED = colors.HexColor("#5b636d")
RULE = colors.HexColor("#d8dce1")
HEAD = colors.HexColor("#f1f3f5")
VERDICT = {
    "Correct": colors.HexColor("#dff3e4"),
    "Partial": colors.HexColor("#fff4cc"),
    "Wrong": colors.HexColor("#fde2e1"),
    "Not scored": colors.HexColor("#eceff2"),
}

base = ParagraphStyle("base", fontName="Helvetica", fontSize=8.6, leading=11, textColor=INK)
small = ParagraphStyle("small", parent=base, fontSize=8, leading=10.2)
bold = ParagraphStyle("bold", parent=small, fontName="Helvetica-Bold")
h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=20, leading=24, spaceAfter=4)
sub = ParagraphStyle("sub", parent=base, fontSize=10, leading=13, textColor=MUTED, spaceAfter=10)
h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=6)
body = ParagraphStyle("body", parent=base, fontSize=10, leading=14, spaceAfter=6)
kpi_num = ParagraphStyle("kn", parent=base, fontName="Helvetica-Bold", fontSize=18, leading=21)
kpi_lab = ParagraphStyle("kl", parent=base, fontSize=8.5, leading=11, textColor=MUTED)

# Round, area, question, verdict, expected, agentaus answer, note
ITEMS = [
    (1, "Trick logic", "A man and a goat, boat holds one man and one goat. Fewest trips?", "Correct",
     "One trip, together", "One trip, they cross together", "Did not fall back on the memorised puzzle"),
    (1, "Letter counting", "Number of r's in 'strawberry raspberry'", "Correct", "6", "6", ""),
    (1, "Arithmetic", "37 x 43 - 1591 / 37", "Correct", "1548", "1548", ""),
    (1, "Logic", "Alice has 3 brothers and 2 sisters. How many sisters does a brother have?", "Correct",
     "3", "3", ""),
    (1, "Calendar", "Day of the week on 1 January 2000", "Correct", "Saturday", "Saturday", ""),
    (1, "Instruction following", "One sentence about Melbourne, exactly 9 words, all lowercase", "Correct",
     "9 lowercase words", "melbourne is a vibrant city with great coffee culture", "Exactly 9 words"),
    (1, "Identity", "Maker, model name and knowledge cutoff", "Not scored",
     "n/a", "Agentaus 1 by Trellis Data; no cutoff given", "Cannot be verified"),
    (2, "Probability", "Monty Hall where the host does not know and opens a goat at random. P(win if switch)?",
     "Correct", "1/2", "1/2", "Correct reasoning on the conditional"),
    (2, "Trick logic", "3 L and 5 L jugs. Fewest steps to measure exactly 5 L?", "Correct",
     "1 (fill the 5 L jug)", "1", ""),
    (2, "Arithmetic", "48271 x 69621, exact", "Correct", "3,360,675,291", "3,360,675,291", "Showed working"),
    (2, "Code", "Output and correctness of a set-based dedupe one-liner on [3,1,3,2,1]", "Correct",
     "[3, 1, 2]; correct", "[3, 1, 2]; correct", "Explained why seen.add() returns None"),
    (2, "Instruction following", "Return ONLY a JSON object (reversed string, vowel count)", "Partial",
     '{"a": "ataD sillerT", "b": 6} and nothing else', "Right JSON, plus explanatory text after it",
     "Broke the 'JSON only' constraint"),
    (2, "Australian knowledge", "What s.44(i) disqualifies; one senator removed in 2017", "Wrong",
     "Foreign allegiance or citizenship. Removed: Ludlam, Waters, Roberts, Nash (and Joyce in the House). "
     "Canavan was found eligible",
     "Named Nash, 'Scott Ludlow' and 'Mattie Canavan' as disqualified",
     "Misspelt name; Canavan was not disqualified"),
    (2, "Calendar", "Day after 28 February 2029", "Correct", "1 March 2029", "1 March 2029", "Noted 2029 is not a leap year"),
    (2, "Identity", "Which open-weights base model is Agentaus 1 fine-tuned from?", "Not scored",
     "n/a", "Declined to disclose", ""),
    (3, "Combinatorics", "Positive integers below 1000 with digit sum 10", "Correct", "63", "63", "Stars and bars, correct"),
    (3, "Number theory", "All positive solutions of x<super>2</super> - 7y<super>2</super> = 1 with x &lt; 1000",
     "Correct", "(8, 3) and (127, 48)", "(8, 3) and (127, 48)", "Used the fundamental solution correctly"),
    (3, "Hallucination trap", "Holding in the fictitious case Kestrel Lane Logistics Pty Ltd v Eastvale City Council (VSC 2021)",
     "Correct", "Say it cannot be found", "Searched, found nothing, said it did not know", "Good calibration"),
    (3, "Current events", "Current Pope and year elected", "Wrong", "Leo XIV, elected 2025",
     "Francis, elected 2013, 'still Pope as of today'", "Stale; had web search but did not use it"),
    (3, "Current events (search)", "2025 AFL Grand Final winner and opponent", "Correct",
     "Brisbane Lions beat Geelong", "Brisbane Lions beat Geelong", "Used web search"),
    (3, "Self-correction", "Recheck its own s.44(i) answer", "Wrong",
     "Fix Ludlam's name and remove Canavan",
     "Fixed 'Ludlam' only; reaffirmed Canavan and cited [2017] HCA 72 (actual: HCA 45)",
     "Doubled down on the substantive error"),
]

# Ultimate round: item, Agentaus verdict, Agentaus conf, Claude verdict, Claude conf, ground truth, note
ULTIMATE = [
    ("U1 Logic grid (verified unique solution)", "Correct", "100", "Correct", "99",
     "Ana Lawyer/Darwin, Ben Manager/Hobart, Cal Engineer/Perth, Dee Designer/Cairns", ""),
    ("U2 False premise: why was Joyce held eligible in Re Canavan?", "Wrong", "80", "Correct", "97",
     "Premise is false: Joyce was disqualified (unanimous)",
     "Agentaus accepted the premise, invented a majority and a Gordon J dissent"),
    ("U3 KOALA acrostic, 6 words a line, no word over 7 letters, no 'e'", "Correct", "100", "Correct", "92",
     "Checked by script", ""),
    ("U4 n &lt;= 2026 with n and n+1 both having an odd number of divisors", "Correct", "100", "Correct", "97",
     "0", ""),
    ("U5 Subsets of {1..15}, no two consecutive, sum divisible by 3", "Wrong", "97", "Correct", "90",
     "536", "Agentaus answered 533; its own working listed 536 under another residue"),
    ("U6 next_palindrome(n), linear time, n up to 10^18", "Correct", "98", "Correct", "95",
     "10,000 random + edge + 2,000 large-value tests", "Both functions passed every test"),
    ("U7 Ledger: net AUD for 'Northgate Co', October", "Correct", "100", "Correct", "93", "15,062.10",
     "Traps: 'Northgate Corp' lookalike, duplicate line"),
    ("U8 Ledger: largest October refund", "Correct", "100", "Correct", "96", "INV111",
     "Trap: larger INV120 is dated September"),
    ("U9 Ledger: number of void entries", "Correct", "100", "Correct", "95", "8", ""),
    ("U10 Ledger: total refunded to Harbour Expo", "Correct", "100", "Correct", "93", "14,766.30", ""),
]

COMPARISON = [
    ("Reasoning and maths", "Rounds 1 to 3 all correct; in round 4, missed one of the three maths items (U5) at 97% confidence",
     "Round 4: all correct", "Moderate",
     "The easy items are saturated for strong models; the harder count separated the two"),
    ("Factual accuracy", "Two serious errors in rounds 1 to 3 (Pope, s.44(i)); accepted the false Joyce premise in round 4",
     "Round 4: rejected the false premise. Not run on rounds 1 to 3", "High",
     "A High Court error is odd for a product sold as Australian and defence grade"),
    ("Self-correction", "Failed: defended its error when asked to recheck", "Not measured here", "High",
     "Fixed the spelling, missed the substance"),
    ("Refusing to invent", "Passed on the fictitious case", "Not measured here", "Moderate",
     "Searched and admitted not knowing"),
    ("Tool use", "Uses web search, but not consistently", "Not measured here", "Moderate",
     "Searched for the AFL and the case, not for the Pope"),
    ("Speed", "About 10 to 40 s per round", "Not measured here", "Moderate", "Fast for multi-part prompts"),
    ("Base model", "Not disclosed; likely a fine-tuned open-weights model plus search", "n/a", "Low to moderate",
     "'Proprietary' probably describes the packaging more than the weights"),
    ("Overall", "Below frontier level", "Ahead in the head-to-head round (10/10 vs 8/10)", "Moderate",
     "31 items is a spot check, not a benchmark"),
]


def P(text, style=small):
    return Paragraph(text, style)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(14 * mm, 9 * mm, "Agentaus 1 vs Claude: spot-check test report, 25 November 2026")
    canvas.drawRightString(doc.pagesize[0] - 14 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def kpis():
    counts = {k: sum(1 for i in ITEMS if i[3] == k) for k in VERDICT}
    scored = counts["Correct"] + counts["Partial"] + counts["Wrong"]
    score = (counts["Correct"] + 0.5 * counts["Partial"]) / scored
    cells = [
        (str(len(ITEMS)), "Questions asked"),
        (str(counts["Correct"]), "Correct"),
        (str(counts["Partial"]), "Partial"),
        (str(counts["Wrong"]), "Wrong"),
        (str(counts["Not scored"]), "Not scored"),
        (f"{score:.0%}", "Score on scored items (partial = half)"),
    ]
    t = Table([[ [P(n, kpi_num), P(l, kpi_lab)] for n, l in cells ]],
              colWidths=[44 * mm] * 6)
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LINEBELOW", (0, 0), (-1, -1), 0.6, RULE),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
             ("LEFTPADDING", (0, 0), (-1, -1), 0)]
    bg = {1: "Correct", 2: "Partial", 3: "Wrong"}
    t.setStyle(TableStyle(style))
    return t, counts, score


def items_table():
    header = [P(h, bold) for h in ["Rd", "Area", "Question", "Verdict", "Expected answer", "Agentaus 1 answer", "Note"]]
    rows = [header]
    for rd, area, q, v, exp, ans, note in ITEMS:
        rows.append([P(str(rd)), P(area), P(q), P(f"<b>{v}</b>"), P(exp), P(ans), P(note)])
    widths = [9, 30, 62, 20, 50, 52, 46]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for r, item in enumerate(ITEMS, start=1):
        style.append(("BACKGROUND", (3, r), (3, r), VERDICT[item[3]]))
    t.setStyle(TableStyle(style))
    return t


def comparison_table():
    header = [P(h, bold) for h in ["Dimension", "Agentaus 1", "Claude (blind control, round 4 only)", "Confidence", "Note"]]
    rows = [header] + [[P(f"<b>{d}</b>"), P(a), P(c), P(conf), P(n)] for d, a, c, conf, n in COMPARISON]
    t = Table(rows, colWidths=[w * mm for w in [38, 68, 50, 26, 87]], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def ultimate_table():
    header = [P(h, bold) for h in ["Item", "Agentaus 1", "Conf.", "Blind Claude", "Conf.", "Ground truth", "Note"]]
    rows = [header]
    for item, av, ac, cv, cc, gt, note in ULTIMATE:
        rows.append([P(item), P(f"<b>{av}</b>"), P(ac), P(f"<b>{cv}</b>"), P(cc), P(gt), P(note)])
    t = Table(rows, colWidths=[w * mm for w in [70, 22, 12, 24, 12, 62, 67]], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for r, it in enumerate(ULTIMATE, start=1):
        style.append(("BACKGROUND", (1, r), (1, r), VERDICT[it[1]]))
        style.append(("BACKGROUND", (3, r), (3, r), VERDICT[it[3]]))
    t.setStyle(TableStyle(style))
    return t


def build():
    doc = SimpleDocTemplate(OUT, pagesize=landscape(A4), leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=13 * mm, bottomMargin=15 * mm,
                            title="Agentaus 1 vs Claude: test report", author="MustBeSimo")
    k, counts, score = kpis()
    story = [
        P("Agentaus 1 vs Claude", h1),
        P("Spot-check of Trellis Data's Agentaus 1 (\"High\" setting) at agentaus.com.au, "
          "run on 25 November 2026. Four rounds, 31 questions; the headline numbers below cover rounds 1 to 3, and page 4 has the head-to-head ultimate round.", sub),
        k,
        Spacer(1, 4),
        P("Verdict", h2),
        P("It got every maths and logic item in rounds 1 to 3 right, but in the harder round it miscounted a "
          "combinatorics question at 97% confidence. It fell down on facts and on checking its own mistakes, though it "
          "avoided trick-question traps and refused to invent a fictitious case. Overall it sits below frontier level "
          "(confidence: moderate).", body),
        P("<b>Key failures.</b> It said Pope Francis is still Pope (Leo XIV was elected in May 2025) despite having "
          "web search. It listed Matt Canavan as disqualified under s.44(i) when the High Court found him eligible, "
          "and when asked to recheck, it fixed only a spelling error, reaffirmed Canavan and cited the wrong case "
          "number.", body),
        P("<b>Ultimate round (page 4).</b> Head to head against a blind Claude control on ten harder items: "
          "Agentaus 1 scored 8/10, Claude 10/10. Agentaus accepted a false legal premise and fabricated a ruling, "
          "and gave a wrong count at 97% confidence. Code, ledger reasoning and constrained writing were level.",
          body),
        P("Comparison with Claude", h2),
        comparison_table(),
        PageBreak(),
        P("Question-by-question results", h2),
        items_table(),
        Spacer(1, 8),
        PageBreak(),
        P("Round 4: the ultimate test, head to head", h2),
        P("Ten harder items with mechanically verifiable answers. The Claude column is a fresh Claude subagent "
          "spawned from the Opus 5.5 grading session, given the identical prompts with no tools, no answers and no "
          "view of Agentaus's replies. <b>Score: Agentaus 1 8/10, blind Claude 10/10.</b> Agentaus's two misses "
          "came at 80% and 97% stated confidence.", body),
        ultimate_table(),
        Spacer(1, 8),
        P("Method note: rounds 1 to 3 were sent as three batched prompts in one conversation, and the ultimate round as "
          "two more prompts in the same conversation. The Canavan recheck (round 3, last item) deliberately prompted "
          "self-verification. Ground truth for arithmetic, code, counting and ledger items was computed in Python "
          "(see the verification folder); legal and current-events items rely on established public record. "
          "Rounds 1 to 3 have no blind Claude control; the comparison there is the grader's judgement.", ParagraphStyle("note", parent=small, textColor=MUTED)),
    ]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(counts, f"{score:.1%}")


if __name__ == "__main__":
    build()
