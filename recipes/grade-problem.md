---
name: grade-problem
description: Mass-grade a single problem from scanned student exam PDFs. Spawn agents specialized by subproblem, collect per-student JSON with TeX comments, merge, and produce printable PDF output.
---

# Mass-Grading a Problem from Scanned Exams

Use this recipe when asked to grade one specific problem across a large set of student PDF scans.

## Prerequisites

Tools that must exist in the project root:
- `pdf2png.py` — renders one PDF page to PNG: `python3 pdf2png.py <pdf> <page_0indexed> [dpi] [outfile]`
- `crop.py` — crops a PNG by percentage: `python3 crop.py <png> <left%> <top%> <width%> <height%>`

Reusable scripts in `recipes/`:
- `recipes/merge_results.py` — merges per-student partial JSONs into a single results file
- `recipes/check_progress.py` — reports which students are missing results

Dependencies: `python-pymupdf` (fitz), `pdflatex`.

## Step 0 — Understand the PDF structure

Before grading, determine:

1. **Which PDF directory** contains the exams. There may be two if the exam was split into booklets.
2. **Which PDF page** the target problem lives on. Render a few sample PDFs with different page counts and visually inspect them with `pdf2png.py` and `crop.py`.
3. **Page count variants** — check if some PDFs are full exams vs. individual booklets. The problem page index may differ between them.
4. **Course split** — identify if students from different courses need different grading (e.g. some do all parts, others only a subset). Check the exam header text.

## Step 1 — Inventory students

List all PDF files and determine for each:
- Student key (filename without `.pdf`)
- Which directory (determines which page to read)
- Which course

## Step 2 — Spawn agents (specialized by subproblem)

**Key principle:** if the problem has P independent parts, spawn P groups of agents, each group responsible for exactly one part across all students. Do not ask a single agent to grade all parts — specialization yields more consistent rubric application.

**Agent count guideline:**
- P groups × ceil(N / batch_size) agents; recommended batch size 15–20 students
- Example: 4 parts × 70 students → 4 groups × 4 agents = 16 agents

**Agent prompt template (adapt per part):**

> You are grading **part (X)** of Problem N from a linear algebra exam.
> Read the grading guidelines in `recipes/grade-p6.md` (or the relevant recipe).
>
> Your students: [list of (key, pdf_path, page_idx, course)].
>
> **What part (X) asks:** [precise statement].
> **Full-credit answer:** [what a 5/5 solution looks like].
> **Only grade part (X)** — ignore other parts even if visible.
>
> For each student:
> 1. Render the exam page: `python3 pdf2png.py <pdf> <page_idx> 200 tmp/<key>_pX.png`
> 2. Locate the student's answer to part (X).
> 3. Assign 0–5 points (or ? if answer is missing/unclear — see guidelines) and write a Czech comment.
>    **Comments must use TeX math** (`$\lambda$`, `$\langle a,b \rangle$`, `$\|x\|$`, `$A^*$`) — no Unicode math symbols.
> 4. Write to `<results_parts_dir>/<key>_pX.json`:
>    ```json
>    {"student": "<key>", "course": "<course>",
>     "Na": {"points": 4, "comment": "Czech TeX comment."}}
>    ```
>    One file per student per part. Omit the file if the student does not attempt this part.
>
> Process students one at a time; write each file before moving to the next.

Create the output directory before spawning agents. Write a one-line script to `tmp/setup.py`:
```
import os; os.makedirs("results-parts", exist_ok=True)
```
then run `python3 tmp/setup.py`.

## Step 3 — Monitor and recover

After agents finish, check progress:

```
python3 recipes/check_progress.py <results_parts_dir> <expected_keys.json>
```

`expected_keys.json` can be a list of student keys, or any JSON object whose top-level keys are student keys. Re-run missing students by spawning additional agents for just those students.

## Step 4 — Merge results

```
python3 recipes/merge_results.py <results_parts_dir> results.json
```

This merges all partial JSONs into a single `results.json`, grouped by student key. Re-running an agent and re-merging is safe — later files overwrite earlier ones for the same part.

## Step 5 — Build PDF table

Write a script `make_pdf_table.py` specific to this exam that reads `results.json` and produces a LaTeX `longtable` (one row per student, columns for each part and total). Compile with pdflatex twice (required for `longtable` page-break computation). See the existing `make_pdf_table.py` in the project root as a reference implementation.

## Step 6 — Build comments PDF

Write a script `make_comments_pdf.py` specific to this exam that reads `results.json` and produces a LaTeX document with one block per student containing the score summary and Czech comments per part. Since agent comments are already valid LaTeX, insert them directly — only apply basic LaTeX escaping to student names and labels. See the existing `make_comments_pdf.py` in the project root as a reference implementation.

Use `mdframed` for colored boxes, `amssymb` + `amsmath` for math. Compile with pdflatex.

## JSON format

Per-student-part file (`<results_parts_dir>/<key>_pa.json`):
```json
{"student": "001_Jan_Novak", "course": "NMAG112",
 "6a": {"points": 4, "comment": "Správně aplikuje $\\langle a_j, b \\rangle = c_j$."}}
```

Merged `results.json`:
```json
{
  "001_Jan_Novak": {
    "student": "001_Jan_Novak", "course": "NMAG112",
    "6a": {"points": 4, "comment": "..."},
    "6b": {"points": 5, "comment": "..."}
  }
}
```

## Common issues

| Symptom | Fix |
|---|---|
| Agent wrote to wrong directory | `cp` the files to the correct parts dir |
| Agent used Unicode math in comments | Re-run those students with an explicit TeX-only instruction |
| pdflatex fails on `\bar` outside math | Wrap in math mode: `$\bar{a}$` |
| pdflatex fails on bare `{` in a comment | Escape as `\{` in the comment, or pre-process in Python |
| Student missing after merge | Check that the agent wrote the correct `"student"` key — it must match the filename prefix |
