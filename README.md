# Agentaus 1 vs Claude Opus 5.5: an independent spot check

Agentaus 1 is the chat model from Trellis Data, marketed as Australia's own model with "defence grade" security at [agentaus.com.au](https://agentaus.com.au). This repo holds an independent test of it from **25 November 2026** (Melbourne time): every prompt, every answer word for word, the scripts that check the answers, and a PDF report.

> **TL;DR.** On logic, code, constrained writing and reading a messy ledger, Agentaus 1 matched Claude. It was weakest when it had to *know* things or *recognise what it didn't know*: it made up a High Court ruling to fit a false premise and kept a factual error when asked to recheck it. It also got one hard counting question wrong at 97% confidence. In the head-to-head round it scored **8/10**; a blind Claude control scored **10/10**.

**Read the report:** [`report/Agentaus_1_vs_Claude_test_report.pdf`](report/Agentaus_1_vs_Claude_test_report.pdf) (4 pages)

---

## Results

### Round 4: the "ultimate test", head to head (blind control)

| Item | Agentaus 1 | Conf. | Blind Claude | Conf. |
|---|---|---|---|---|
| U1 Logic grid (checked to have exactly one solution) | ✅ | 100 | ✅ | 99 |
| U2 **False premise:** "why was Joyce held eligible in *Re Canavan*?" | ❌ made up a ruling | 80 | ✅ rejected the premise | 97 |
| U3 KOALA acrostic: 6 words a line, no word over 7 letters, no letter "e" | ✅ | 100 | ✅ | 92 |
| U4 n ≤ 2026 with n and n+1 both having an odd number of divisors (answer 0) | ✅ | 100 | ✅ | 97 |
| U5 Subsets of {1..15} with no two consecutive numbers and a sum divisible by 3 (answer 536) | ❌ said 533 | 97 | ✅ | 90 |
| U6 `next_palindrome(n)` up to 10¹⁸: 10,000 random tests, edge cases and large values | ✅ | 98 | ✅ | 95 |
| U7 to U10: 37-entry multi-currency ledger, with a lookalike client name, a duplicate line, a refund outside the date range and voided entries | ✅ 4/4 | 100 | ✅ 4/4 | 93 to 96 |
| **Total** | **8/10** | | **10/10** | |

### Rounds 1 to 3 (21 items, Agentaus only)

15 correct, 1 partial, 3 wrong, 2 not scored (questions about its own model) → **82%** on scored items, counting the partial as half.

| Failure | What happened |
|---|---|
| Current Pope | Said Francis is "still Pope as of today". Leo XIV was elected in May 2025. It had web search and didn't use it for this question. |
| Section 44(i) senators | Said Matt Canavan was disqualified in 2017. The High Court found him eligible. It also misspelled Ludlam. |
| Asked to recheck that answer | Fixed the spelling only, repeated the Canavan claim, and gave the wrong citation ([2017] HCA 72; the real one is HCA 45). |
| "Return ONLY JSON" | Right JSON, but with extra text after it. |

Strengths: it avoided the classic trick-question traps, got exact arithmetic right, and **refused to invent a fictitious court case** after searching for it.

The full table, one row per question, is in [`results/results.csv`](results/results.csv).

### Evidence

Screenshots taken from the Agentaus conversation on the night of the test, cropped to the answer only:

- [`evidence/round4_U2_invented_joyce_ruling.png`](evidence/round4_U2_invented_joyce_ruling.png): Agentaus describes a majority holding Joyce eligible, with a Gordon J dissent. In fact the Court unanimously held him ineligible.
- [`evidence/round3_pope_and_canavan_recheck.png`](evidence/round3_pope_and_canavan_recheck.png): "Pope Francis … still Pope as of today", plus the recheck that repeats the Canavan claim and cites HCA 72.

---

## What this does and doesn't show

**Findings (confidence in brackets):**
- **Facts and calibration are the main gap** (high). Its factual errors outnumber its reasoning errors, though it did miss one hard count (U5). Both of its misses in the ultimate round came with confidence of 80% or more, so its confidence figures don't help you spot its errors.
- **It doesn't reliably correct itself** (moderate to high). It repeated a factual error after being asked directly to check it, which matters for any workflow that relies on "ask it to double-check".
- **Self-contained tasks are fine** (moderate). With complete data and a clear spec (code, ledgers, constrained writing), it was level with Claude.
- **It's probably a fine-tuned open-weights model with web search added** (low to moderate). It declined to name its base model.

**Limits:**
- **Small sample.** 31 items is a spot check, not a benchmark, and one more miss either way would change the headline score.
- **The control is from the same family as the grader.** The blind control is a Claude subagent spawned from the Claude Opus 5.5 grading session. Subagents inherit the parent model by default, but this wasn't checked separately. It had no tools, no answers and no view of Agentaus's replies, though it is still Claude. Rounds 1 to 3 had no blind control.
- **The questions lean towards things Claude knows well.** Australian legal facts and recent events are part of the test because a product marketed as Australian should handle them.
- **This is one point in time.** Hosted models change. These results describe Agentaus 1 on the "High" setting on 25 November 2026.
- All prompts went into **one conversation**, so earlier turns could have influenced later ones. Round 3 item 6 relied on this on purpose.

---

## Reproduce it

1. Paste the prompts from [`prompts/prompts.md`](prompts/prompts.md) into any model, in order.
2. Check the computable answers:

```bash
python3 verification/rounds_1_to_3_ground_truth.py          # arithmetic, code, counting
python3 verification/ultimate_part1_ground_truth.py         # logic-grid uniqueness, divisor and subset counts
python3 verification/ultimate_part2_ledger_ground_truth.py  # regenerates the ledger (fixed seed) and all four answers
python3 verification/check_poems_and_code.py                # tests both acrostics and both palindrome functions
```

3. Rebuild the PDF (requires `reportlab`): `cd report && python3 build_report.py`

**Names changed after the test:** for confidentiality, names were replaced in every file (the prompts, both sets of answers, the scripts and the report): the ledger clients, now "Harbour Expo", "Riverside Events", "Northgate Co" and its lookalike "Northgate Corp", and the parties to the fictitious case, now "Kestrel Lane Logistics Pty Ltd v Eastvale City Council". They are only labels, so no answer or score changes, and the ledger script still regenerates the ledger exactly as printed in `prompts/prompts.md`. Nothing else in the transcripts was edited.

The non-computable items (Pope, *Re Canavan*, AFL Grand Final) rely on public record: Leo XIV was elected on 8 May 2025, and *Re Canavan* [2017] HCA 45 disqualified Joyce, Nash, Ludlam, Waters and Roberts, and held Canavan and Xenophon eligible.

## Repo layout

```
evidence/                           screenshots of the key Agentaus answers
prompts/prompts.md                  every prompt, verbatim
responses/agentaus_1.md             Agentaus 1 answers, verbatim
responses/claude_blind_control.md   blind Claude control answers, verbatim
results/results.csv                 one row per item with verdicts and confidence
verification/                       ground-truth and checking scripts
report/                             PDF report and the script that builds it
```

---

Independent test with no affiliation to Trellis Data or Anthropic. The tests were designed, run and graded with Claude Opus 5.5 under the direction of [@mustbesimo](https://github.com/MustBeSimo). Corrections and reruns are welcome: open an issue with your transcript.

## Licence

[MIT](LICENSE). Agentaus 1's answers, in `responses/agentaus_1.md` and `evidence/`, are quoted for review and are not covered by this licence.
