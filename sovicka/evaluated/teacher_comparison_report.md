# Teacher–model grading comparison

Date: 2026-09-11

## Executive summary

The model is a useful second reader, but it is not yet a reliable replacement
for teacher grading. Across all 2,064 held-out submissions, it agrees exactly
with the recorded teacher score in 67.0% of cases, is within 0.5 point in 87.1%,
and is within 1 point in 95.7%. The mean absolute error is 0.270 points on the
0–4 scale, and quadratic weighted agreement is 0.445.

These aggregate results require an important qualification: 78.0% of the
held-out teacher grades are 4/4. Consequently, an `always predict 4` baseline
beats the model on exact agreement, mean absolute error, and RMSE. The model
does provide real ranking and error-detection signal that the constant baseline
does not, but its deductions are not calibrated closely enough to the recorded
teacher policy to be applied automatically.

Manual inspection of large disagreements found three distinct phenomena:

1. genuine model errors, especially visual or attachment-identification errors;
2. genuine or likely teacher errors or unusually lenient grading; and
3. target mismatch, where the teacher knew about swapped files, resubmissions,
   lateness, or other context unavailable to the model.

The teacher scores should therefore be regarded as noisy operational labels,
not as unquestionable mathematical ground truth. The most appropriate current
use of the model is as a second-reader and discrepancy detector, followed by
human adjudication.

## Data and methodology

The comparison uses:

- teacher exchanges and scores from [`all_exchange`](../all_exchange/);
- model scores and justifications from the evaluation JSON files in this
  directory;
- training examples from [`examples`](../examples/); and
- the split procedure in [`prepare_data.py`](../prepare_data.py).

The model evaluation files were joined to teacher records by homework filename
and anonymized student identifier. All 2,064 predictions matched exactly one
teacher record.

### Dataset audit

| Stage | Records |
| --- | ---: |
| Raw `all_exchange` records | 2,558 |
| Excluded multi-turn or nonstandard exchanges | 54 |
| Eligible single-interaction records | 2,504 |
| Training examples (20 per homework part) | 440 |
| Held-out predictions | 2,064 |
| Successfully matched teacher/model pairs | **2,064** |

Additional integrity checks found that:

- no held-out teacher grade is missing;
- all 2,558 raw records contain a score;
- in every raw record, the final `Points:` message agrees with the JSON
  `points` field; and
- the model's `correct` field is consistent with its 4/4 score convention.

Metrics are computed on the 2,064 matched held-out submissions only. Bias is
defined as `model score − teacher score`. The uncertainty intervals below use
10,000 bootstrap samples resampling whole homework parts, rather than treating
all submissions as independent. Quadratic weighted kappa uses squared numerical
distance on the 0–4 scale. The case review is a targeted qualitative audit and
is not a complete independent regrading of every disagreement.

## Important split-design limitation

The 20 training examples for each homework were selected round-robin across
the available score buckets. This deliberately exposes the model to rare error
classes, but it produces a strong label-prior shift:

| Dataset | Full-credit records | Full-credit proportion |
| --- | ---: | ---: |
| Training examples | 133 / 440 | **30.2%** |
| Held-out test set | 1,610 / 2,064 | **78.0%** |
| All eligible records | 1,743 / 2,504 | **69.6%** |

Rare low-score submissions were disproportionately moved into the training
set, leaving a ceiling-heavy held-out set. This is not label leakage into the
model's predictions, but it is not an IID train/test split. It weakens the
interpretability of raw accuracy and calibration as estimates of future
performance.

## Overall quantitative results

| Metric | Result |
| --- | ---: |
| Matched submissions | 2,064 |
| Teacher mean score | 3.800 |
| Model mean score | 3.737 |
| Bias (model − teacher) | **−0.063** |
| Mean absolute error | **0.270** |
| Median absolute error | 0.000 |
| RMSE | **0.558** |
| Exact score agreement | **66.96%** |
| Agreement within 0.5 point | **87.11%** |
| Agreement within 1 point | **95.69%** |
| Pearson correlation | 0.455 |
| Spearman correlation | 0.278 |
| Quadratic weighted kappa | **0.445** |
| Unweighted kappa | 0.164 |
| R² | −0.340 |
| Maximum absolute disagreement | 4.0 |

The negative R² means that a constant prediction equal to the held-out teacher
mean would have lower squared error. This result is partly driven by the narrow,
ceiling-heavy teacher distribution and does not imply that the constant model
has useful grading discrimination.

### Homework-cluster uncertainty

Approximate 95% cluster-bootstrap intervals are:

| Metric | Point estimate | 95% interval |
| --- | ---: | ---: |
| Bias | −0.063 | −0.160 to +0.033 |
| Mean absolute error | 0.270 | 0.222 to 0.323 |
| Exact agreement | 67.0% | 57.7% to 74.5% |
| Within 0.5 point | 87.1% | 84.2% to 89.6% |
| Quadratic weighted kappa | 0.445 | 0.240 to 0.587 |

The interval around bias includes zero because substantial positive and
negative homework-specific offsets cancel in the combined result.

### Score distributions

| Score | Teacher count | Model count |
| ---: | ---: | ---: |
| 0 | 4 | 6 |
| 0.5 | 0 | 0 |
| 1 | 9 | 13 |
| 1.5 | 4 | 11 |
| 2 | 40 | 44 |
| 2.5 | 22 | 58 |
| 3 | 120 | 176 |
| 3.5 | 255 | 203 |
| 4 | 1,610 | 1,553 |

The model assigns fewer full-credit scores overall, but this does not mean it
is uniformly stricter. Conditional on a teacher score below 4, the model is on
average 0.361 points more generous. Conditional on a teacher score of 4, the
model is on average 0.182 points stricter. It compresses the teacher distinction
between 3.5 and 4: both groups receive a mean model score of approximately
3.818.

### Difference distribution

| Model − teacher | Count | Share |
| ---: | ---: | ---: |
| −4.0 | 3 | 0.15% |
| −3.0 | 5 | 0.24% |
| −2.5 | 8 | 0.39% |
| −2.0 | 12 | 0.58% |
| −1.5 | 33 | 1.60% |
| −1.0 | 121 | 5.86% |
| −0.5 | 203 | 9.84% |
| 0.0 | 1,382 | 66.96% |
| +0.5 | 213 | 10.32% |
| +1.0 | 56 | 2.71% |
| +1.5 | 13 | 0.63% |
| +2.0 | 14 | 0.68% |
| +3.5 | 1 | 0.05% |

There are 89 disagreements larger than 1 point, affecting 68 students. Of
these, 43 differ by at least 2 points. The model scores higher in 297 records,
lower in 385 records, and exactly matches in 1,382 records.

## Baselines and discrimination

| Predictor | Exact | Within 0.5 | MAE | RMSE |
| --- | ---: | ---: | ---: | ---: |
| Model | 66.96% | 87.11% | 0.270 | 0.558 |
| Always predict 4 | **78.00%** | **90.36%** | **0.200** | **0.522** |

The constant baseline wins these raw metrics because of class imbalance, but
it has no discrimination and quadratic weighted kappa is zero. The model's
full-credit classification performance is:

| Metric | Result |
| --- | ---: |
| Full-credit precision | 83.1% |
| Full-credit recall | 80.2% |
| Full-credit specificity | 42.3% |
| Full-credit F1 | 81.6% |
| Balanced accuracy | 61.2% |
| AUC for teacher full credit | 0.627 |

When the model predicts below 4, only 37.6% of those records also receive below
4 from the teacher. Conversely, the model identifies 42.3% of all teacher
non-full-credit records. Model deductions are therefore informative review
signals, but not reliable automatic penalties.

## Per-homework results

`Δ` is the model mean minus the teacher mean. A dagger marks homework parts for
which every held-out teacher score is 4, making within-homework correlation and
discrimination unidentifiable.

| Homework | N | Teacher mean | Model mean | Δ | MAE | Exact | Within 0.5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DU 01.1 | 140 | 3.957 | 3.796 | −0.161 | 0.189 | 79.3% | 90.0% |
| DU 01.2 | 129 | 3.516 | 3.500 | −0.016 | 0.287 | 71.3% | 82.9% |
| DU 02.1 | 144 | 3.990 | 3.858 | −0.132 | 0.139 | 81.9% | 90.3% |
| DU 02.2 | 137 | 3.832 | 3.697 | −0.135 | 0.142 | 84.7% | 90.5% |
| DU 03.1 | 126 | 3.595 | 3.893 | **+0.298** | 0.345 | 68.3% | 84.1% |
| DU 03.2 | 125 | 3.728 | 3.452 | **−0.276** | 0.308 | 50.4% | 89.6% |
| DU 04.1 | 138 | 3.779 | 3.851 | +0.072 | 0.246 | 59.4% | 91.3% |
| DU 04.2 | 129 | 3.810 | 3.880 | +0.070 | 0.194 | 76.0% | 87.6% |
| DU 05.1† | 134 | 4.000 | 3.791 | −0.209 | 0.209 | 79.1% | 85.1% |
| DU 05.2 | 133 | 3.590 | 3.959 | **+0.368** | 0.436 | **18.0%** | **99.2%** |
| DU 06.1 | 133 | 3.955 | 3.857 | −0.098 | 0.113 | 86.5% | 91.0% |
| DU 06.2 | 126 | 3.730 | 3.837 | +0.107 | 0.298 | 54.0% | 91.3% |
| DU 07.1† | 94 | 4.000 | 3.532 | **−0.468** | 0.468 | 71.3% | 76.6% |
| DU 07.2 | 103 | 3.757 | 3.840 | +0.083 | 0.306 | 68.9% | 78.6% |
| DU 08.1† | 55 | 4.000 | 3.655 | **−0.345** | 0.345 | 65.5% | 83.6% |
| DU 08.2 | 59 | 3.559 | 3.254 | **−0.305** | 0.339 | 67.8% | 76.3% |
| DU 09.1 | 42 | 3.357 | 3.083 | −0.274 | **0.679** | 23.8% | 66.7% |
| DU 09.2 | 23 | 3.652 | 3.217 | **−0.435** | **0.609** | 34.8% | 65.2% |
| DU 10.1† | 29 | 4.000 | 3.897 | −0.103 | 0.103 | 79.3% | 100.0% |
| DU 10.2† | 35 | 4.000 | 3.743 | −0.257 | 0.257 | 65.7% | 88.6% |
| DU 11.1† | 19 | 4.000 | 3.842 | −0.158 | 0.158 | 84.2% | 84.2% |
| DU 11.2† | 11 | 4.000 | 3.818 | −0.182 | 0.182 | 81.8% | 81.8% |

The unweighted macro-average across homework parts is 66.0% exact agreement,
85.2% within 0.5 point, and MAE 0.289. Homework-specific mean offsets account
for approximately 14.7% of total squared residual variation, so per-homework
calibration would help but would not resolve most record-level disagreement.

Notable patterns include:

- DU 05.2's very low exact agreement is primarily a systematic 4-versus-3.5
  distinction, not a large mathematical discrepancy; 99.2% are within 0.5.
- DU 03.1 contains many model-over-teacher disagreements, while DU 03.2 moves
  strongly in the opposite direction.
- DU 07.1 and DU 08.1 have universally perfect teacher scores despite multiple
  substantive mathematical defects identified by the model.
- DU 09.1 and DU 09.2 have the largest average absolute disagreements.
- Seven homework parts have no teacher-score variation in the held-out data.

## Comparison of justifications

### Teacher-justification availability

There is no direct matched justification comparison to perform. None of the
2,064 held-out records contains a substantive teacher remark, and none of the
440 selected training examples contains one either. Sixteen teacher remarks
exist only in the 54 excluded multi-turn exchanges.

Those excluded remarks are nevertheless informative about the operational
grading target. They show cases involving:

- a mathematically correct answer receiving zero because it was late;
- acceptance of two homework parts submitted in the opposite order;
- a penalty for using a theorem explicitly forbidden by the assignment;
- reassessment after a pair-submission misunderstanding; and
- detailed concern about proof gaps and invalid logical implications.

This confirms that the recorded teacher score can depend on contextual and
administrative information absent from the model input.

### Model-justification specificity

The model produced 628 unique justifications for 2,064 submissions. A total of
1,436 records reuse a justification found elsewhere. Repetition is reasonable
when many correct solutions follow the same standard argument, but several
large template groups receive heterogeneous teacher scores:

| Homework/template group | Repetitions | Teacher-score distribution |
| --- | ---: | --- |
| DU 05.2 full-credit construction | 130 | 107 × 3.5, 23 × 4 |
| DU 06.2 full-credit diagonalization | 111 | 5 × 3, 41 × 3.5, 65 × 4 |
| DU 03.1 full-credit equivalence proof | 109 | 9 × 2, 17 × 3.5, 83 × 4 |
| DU 04.2 full-credit minimum-norm solution | 114 | scores from 2 through 4 |

This can reflect teacher inconsistency or hidden policy, but manual inspection
also shows that the model sometimes overgeneralizes superficially similar
solutions and misses proof-quality differences. A stronger justification should
cite the actual decisive equation, page, or argument rather than only summarize
the expected correct method.

## Manual audit of representative disagreements

The following examples were checked against the actual submission content and
problem statement. They illustrate failure modes rather than estimate their
population frequencies.

| Submission | Teacher / model | Audit finding |
| --- | ---: | --- |
| DU 07.2 / 3001 | 4 / 0 | **Clear model error.** The page is visibly labeled 7.2 and correctly solves the polynomial-operator problem. The model falsely claimed that it solved 7.1. |
| DU 01.1 / 3221 | 4 / 0 | The attachment solves 1.2, while the same student's other slot contains 1.1. This is mainly a paired-context mismatch: the teacher apparently accepted swapped files, while the model graded each slot literally. |
| DU 05.2 / 3131 | 4 / 0 | The file visibly solves 5.1. A teacher remark in the paired exchange explicitly acknowledges that the student swapped the two parts. The isolated model lacked that context. |
| DU 08.1 / 3057 | 4 / 1.5 | The proposed eigenvector `(2,−3,5)` does not satisfy `Av=2v`. The model's concrete diagnosis is correct; full teacher credit appears mathematically questionable or very lenient. |
| DU 07.1 / 2900 | 4 / 1 | The claimed zero-intersection condition and dimension formula are incorrect. The model identifies a substantive mathematical problem, although 1/4 may be harsher than necessary. |
| DU 01.2 / 2815 | 2 / 4 | The write-up does not cleanly establish necessity. The model's statement that both implications were proved is overconfident; the teacher's lower score is defensible. |
| DU 03.1 / 2377 | 2 / 4 | The submission appears to give a valid matrix argument using `AU=V`, `UᵀU=VᵀV`, and invertibility of `U`. The model's full score looks more defensible than the unexplained teacher 2. |
| DU 04.2 / 3062 | 2 / 4 | The numerical minimum-norm solution is correct, but the key minimum-norm characterization is largely asserted. This is plausibly a rigor/rubric difference, with the model accepting more than the teacher. |
| DU 09.1 / 3205 | 0 / 3.5 | The recurrence, eigenstructure, growth threshold, and limiting ratio are substantially correct; the model notes a boundary omission. No visible mathematical reason explains a zero, suggesting missing administrative context or a questionable teacher label. |

This audit provides direct evidence for all three major causes of disagreement:
model error, human grading error or leniency, and missing contextual features.

## Recommended next experiment

### 1. Adjudicate severe disagreements

Blindly regrade the 89 cases differing by more than 1 point, beginning with the
43 that differ by at least 2 points. Of the 89 severe cases, 57 (64%) are
concentrated in DU 01.2, 03.1, 07.1, 08.1, and 08.2. The adjudicator should not
see which score came from the model or the original teacher.

### 2. Separate mathematical and operational labels

Record two outputs for each submission:

1. a mathematical-content score; and
2. an operational score after lateness, wrong-slot, collaboration, and other
   course policies.

This would distinguish model correctness failures from unavailable policy
information.

### 3. Preserve contextual features

Future model input should include paired homework threads, timestamps,
resubmission history, teacher-visible notes, and explicit policy flags. Apparent
task swaps should trigger an abstention or cross-part lookup rather than an
automatic zero.

### 4. Create an untouched representative test set

Use a random, student-grouped, or chronological holdout that is not selected
using the labels. Balanced rare-score examples can still be used during
training, but calibration must use sampling weights or a separate representative
validation set.

### 5. Strengthen evidence-linked grading

Every deduction should identify the exact equation, page, or logical step that
causes it. Simple claims such as eigenvector identities, matrix products,
interpolation constraints, characteristic polynomials, and numerical solutions
should be checked automatically when possible. The model should expose
uncertainty and abstain on illegible scans or ambiguous attachments.

## Conclusion

As a predictor of recorded teacher scores, the current model is not competitive
with the ceiling-heavy constant baseline on raw loss. As a mathematical second
opinion, it is valuable: it catches real algebraic and proof errors and supplies
actionable feedback. Its main weaknesses are homework-specific calibration,
overgeneralized full-credit templates, insufficient sensitivity to proof rigor,
and occasional catastrophic visual or file-association mistakes.

The teacher labels are also imperfect and sometimes measure more than
mathematical correctness. A blind adjudication study with context-complete,
dual-purpose labels is the necessary next step before drawing stronger claims
about either grader's true accuracy or deploying model scores without human
review.
