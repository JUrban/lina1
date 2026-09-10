---
name: grade-p7
description: Grading guidelines specific to Úloha 7 of the linear algebra final exam. Covers problem statement, grading principles, full-credit solutions, and mathematical pitfalls.
---

# Grading Guidelines — Úloha 7

Use this skill when grading or instructing agents to grade **Úloha 7** from the June 2026 final exam. Pair with `/grade-problem` for the operational workflow.


## Exam structure

- **NMAG 112** (zimní i letní semestr, Lineární algebra 2): answers all three parts (a, b, c). **Max 18 points.**
- **NMAG 114** (Lineární algebra pro fyziky): answers only parts (a) and (b). Parts (c) and (d) are marked *"Pouze pro NMAG 112"* — do not grade them for NMAG 114 students. **Max 10 points.**

Each part is worth **0–6 points** for NMAG112, or **0-8 points** for NMAG114, or **?** (see below).

## Grading principles

**Score distribution:** The default score for any part is **0** (no valid progress) or **6** (complete, correct proof). Any intermediate score (1–7) must be explicitly justified in the comment — if you cannot articulate a precise reason, default to 0 or 6 (or 8 for NMAG114).

**Giving 5:** Imagine the student coming to argue it should be 6. You must be able to defend your deduction with a concrete, identifiable error or gap in an otherwise complete proof. If you cannot pinpoint what is wrong, give 6.

**Giving 1 or 2:** Imagine the lecturer arguing it should be 0. You must be able to show that the student made *clear, meaningful progress toward the solution* — not merely that they wrote something relevant. If you cannot, give 0.

**Degenerate and boundary cases:** Missing a degenerate case (e.g. $v = 0$, $n = 0$, $\lambda = 0$) is a real mathematical error — the student's argument as written may be literally false in those cases. Deduct a point even if the main argument is otherwise correct. A student who truly understands the material will accept the deduction, because they wrote something that is mathematically false under certain circumstances. Degenerate cases are generally important in linear algebra and should not be waved away as trivial.

**What does not earn points:**
- Stating the problem's assumptions as if that were progress.
- Claiming the conclusion without properly arriving at it.
- Citing a relevant theorem, concept, or keyword without applying it correctly.
- Doing something mathematically valid that stays entirely within the problem's setup without actually advancing toward the goal (e.g. writing out definitions, restating what "normal" means, or writing $A^*A = AA^*$ once and then stopping).

**Partial credit requires genuine forward movement:** Award intermediate points only when the student has demonstrably moved closer to a complete proof — not merely for having started in a plausible direction.

**Mathematical precision:**
- Build a precise mathematical understanding of what the problem requires before assigning a score. Do not judge by general impression or intuition.
- Be especially strict toward students who write mathematically false or nonsensical statements, or who confuse assumptions with what needs to be proved. Such errors outweigh any surrounding correct work.
- On the other hand, appreciate students who clearly understand the argument and are merely writing quickly, even if some steps are omitted. Distinguish them sharply from students who have only a rough idea of the proof without command of the details.

**Insufficient data — score '?':**
- If a student refers to another page (e.g. "viz strana 17") and the answer cannot be found in the PDF, assign **?** points with a Czech comment noting the missing page.
- Before concluding a page is missing: PDF page indices and the printed page labels are often offset. A student writing "viz strana 17" may mean the page *labeled* 17, which could be a different PDF page index. Render all pages of the PDF and check the page labels before giving up.

## Mathematical pitfalls

These are patterns observed in students' solutions to this exam. They are stated without reference to specific parts because the same patterns recur across different problems and future exams.

**Claiming the conclusion:** Writing down the formula or statement to be proved and treating it as a result, without any derivation. Earns **0** regardless of whether the formula is correct.

**Confusing hypothesis and conclusion:** Using the statement to be proved as a step in its own proof. Be strict — this is a fundamental logical error.

**Incorrect proof via determinants:** Showing that a certain value is an eigenvalue of a matrix (via $\det = 0$) when the problem asks to prove something about a *specific* eigenvector. These are different claims: existence of an eigenvalue does not identify which vector is the eigenvector.

**Asserting one computation follows from another by symmetry:** Acceptable only if the student clearly understands both computations and the symmetry is genuinely obvious. If there is any doubt, treat it as a gap.

**Wrong inner product scalars in complex spaces:** Proofs that implicitly assume the inner product is real-valued (e.g. choosing a real optimal parameter in a minimization argument) are incomplete for complex inner product spaces.

**Not invoking linearity explicitly:** In arguments involving $\langle \cdot, \sum c_i a_i \rangle$, linearity must be at least implicitly acknowledged. Whether omitting it costs a point depends on whether the student otherwise clearly knows what they are doing.

**False statements about orthonormality:** Claiming $\langle a_i, a_j \rangle = 1$ for all $i, j$ (instead of $\delta_{ij}$) is a mathematically false statement — be strict.

**"Nestíhám" (ran out of time):** Award partial credit strictly proportional to how far the proof actually got, applying the same genuine-progress standard as always.

## PDF page reference

Use `python3 pdf2png.py <pdf> <idx> 200 out.png` to render, then `python3 crop.py out.png 0 50 100 50` to see the lower half of the page where problem 6 typically appears. When a student refers to a specific page by printed label, check that label against all pages of the PDF — do not assume the label matches the index.
