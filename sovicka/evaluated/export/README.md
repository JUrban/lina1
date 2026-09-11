# Homework evaluation dashboard

This export contains **2,064 evaluations** across **22 homework parts**.

## Downloads

- [All individual evaluations (CSV)](all_evaluations.csv)
- [Homework-level summary (CSV)](homework_summary.csv)

Both files use UTF-8 encoding and comma-separated, double-quoted fields. The combined CSV keeps student-facing `feedback` separate from evaluator-only `justification`.

## Homework overview

| Homework | Submissions | Average / 4 | Median / 4 | Fully correct | Full-credit rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| [DU 01.1](markdown/du01_1.md) | 140 | 3.796 | 4 | 111 | 79.3% |
| [DU 01.2](markdown/du01_2.md) | 129 | 3.5 | 4 | 78 | 60.5% |
| [DU 02.1](markdown/du02_1.md) | 144 | 3.858 | 4 | 118 | 81.9% |
| [DU 02.2](markdown/du02_2.md) | 137 | 3.697 | 4 | 96 | 70.1% |
| [DU 03.1](markdown/du03_1.md) | 126 | 3.893 | 4 | 109 | 86.5% |
| [DU 03.2](markdown/du03_2.md) | 125 | 3.452 | 3.5 | 55 | 44% |
| [DU 04.1](markdown/du04_1.md) | 138 | 3.851 | 4 | 108 | 78.3% |
| [DU 04.2](markdown/du04_2.md) | 129 | 3.88 | 4 | 114 | 88.4% |
| [DU 05.1](markdown/du05_1.md) | 134 | 3.791 | 4 | 106 | 79.1% |
| [DU 05.2](markdown/du05_2.md) | 133 | 3.959 | 4 | 130 | 97.7% |
| [DU 06.1](markdown/du06_1.md) | 133 | 3.857 | 4 | 111 | 83.5% |
| [DU 06.2](markdown/du06_2.md) | 126 | 3.837 | 4 | 111 | 88.1% |
| [DU 07.1](markdown/du07_1.md) | 94 | 3.532 | 4 | 67 | 71.3% |
| [DU 07.2](markdown/du07_2.md) | 103 | 3.84 | 4 | 92 | 89.3% |
| [DU 08.1](markdown/du08_1.md) | 55 | 3.655 | 4 | 36 | 65.5% |
| [DU 08.2](markdown/du08_2.md) | 59 | 3.254 | 4 | 31 | 52.5% |
| [DU 09.1](markdown/du09_1.md) | 42 | 3.083 | 3 | 3 | 7.1% |
| [DU 09.2](markdown/du09_2.md) | 23 | 3.217 | 3.5 | 6 | 26.1% |
| [DU 10.1](markdown/du10_1.md) | 29 | 3.897 | 4 | 23 | 79.3% |
| [DU 10.2](markdown/du10_2.md) | 35 | 3.743 | 4 | 23 | 65.7% |
| [DU 11.1](markdown/du11_1.md) | 19 | 3.842 | 4 | 16 | 84.2% |
| [DU 11.2](markdown/du11_2.md) | 11 | 3.818 | 4 | 9 | 81.8% |
| **Overall** | **2064** | **3.737** | **4** | **1553** | **75.2%** |

## Overall score distribution

| Points | Students |
| ---: | ---: |
| 0 | 6 |
| 0.5 | 0 |
| 1 | 13 |
| 1.5 | 11 |
| 2 | 44 |
| 2.5 | 58 |
| 3 | 176 |
| 3.5 | 203 |
| 4 | 1553 |

## Presentation notes

Each homework link opens a web-friendly Markdown page. Individual student rows are collapsible, and the evaluator-only justification is placed in a separate nested disclosure beneath the Czech student feedback.

The files are generated from the evaluation JSON files by running:

```bash
node ../export_evaluations.mjs
```
