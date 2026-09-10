# Homework evaluation output

Each `duNN_M.json` file mirrors the student identifiers in the corresponding
`to_eval/duNN_M.json` file. Every record contains:

- `points`: score on the 0--4 homework scale;
- `correct`: `true` only for a fully correct solution (therefore normally only
  when `points` is `4.0`);
- `justification`: evaluator-only reasoning, not intended for the student;
- `feedback`: detailed student-facing feedback in Czech. This field does not
  disclose the evaluator-only justification.

Scores are calibrated against the 20 labelled examples for the same homework
part and use the general mathematical-proof principles in `recipes/`.

