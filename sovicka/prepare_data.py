#!/usr/bin/env python3
"""
Prepare examples/ and to_eval/ directories from problems/ JSON files.

examples/  — 20 entries per problem with student solution + teacher evaluation,
             distributed evenly across point values.
to_eval/   — remaining valid entries with only the student solution (no eval).
"""

import json
import os
import random
import re
from collections import defaultdict
from pathlib import Path

PROBLEMS_DIR = Path("all_exchange")
EXAMPLES_DIR = Path("examples")
TO_EVAL_DIR = Path("to_eval")
EXAMPLES_PER_PROBLEM = 20
SEED = 42


def is_single_interaction(msgs: list) -> bool:
    """Return True if msgs follow the pattern S+ T (all student messages first,
    then exactly one teacher message at the end, nothing after)."""
    if not msgs:
        return False
    first_teacher = next((i for i, m in enumerate(msgs) if m["is_teacher"]), None)
    if first_teacher is None:
        return False  # no teacher response yet
    teacher_msgs = msgs[first_teacher:]
    if len(teacher_msgs) != 1:
        return False
    student_msgs = msgs[:first_teacher]
    if any(m["is_teacher"] for m in student_msgs):
        return False
    return True


def extract_teacher_remark(msg: str) -> str | None:
    """Return teacher's text with the 'Points: X.XX' line stripped out, or None if empty."""
    cleaned = re.sub(r"\bPoints:\s*[\d.]+\b", "", msg)
    cleaned = cleaned.strip().strip("\t").strip()
    return cleaned if cleaned else None


def build_solution(student_msgs: list) -> list:
    """Build solution list from student messages, skipping deleted posts."""
    result = []
    for m in student_msgs:
        if "*Post deleted by its author.*" in m["msg"]:
            continue
        entry = {"msg": m["msg"].strip()}
        if m["attachment"]:
            entry["attachment"] = m["attachment"]
        result.append(entry)
    return result


def select_examples(valid: dict, n: int, rng: random.Random) -> dict:
    """Select up to n entries distributed evenly across point values."""
    by_points = defaultdict(list)
    for student_id, entry in valid.items():
        by_points[entry["points"]].append(student_id)

    for bucket in by_points.values():
        rng.shuffle(bucket)

    # Round-robin across sorted point buckets until we have n
    sorted_buckets = sorted(by_points.keys())
    buckets = [list(by_points[p]) for p in sorted_buckets]
    selected_ids = []
    while len(selected_ids) < n and any(buckets):
        for bucket in buckets:
            if bucket and len(selected_ids) < n:
                selected_ids.append(bucket.pop(0))

    return {sid: valid[sid] for sid in selected_ids}


def process_problem(path: Path, rng: random.Random) -> tuple[dict, dict]:
    """Return (examples_data, to_eval_data) for one problem file."""
    with open(path) as f:
        raw = json.load(f)

    valid = {}
    for student_id, entry in raw.items():
        msgs = entry["msgs"]
        if not is_single_interaction(msgs):
            continue
        if entry["points"] is None:
            continue
        valid[student_id] = entry

    examples_raw = select_examples(valid, n=EXAMPLES_PER_PROBLEM, rng=rng)

    examples_out = {}
    for sid, entry in examples_raw.items():
        msgs = entry["msgs"]
        student_msgs = [m for m in msgs if not m["is_teacher"]]
        teacher_msg = next(m for m in msgs if m["is_teacher"])
        remark = extract_teacher_remark(teacher_msg["msg"])
        record = {
            "solution": build_solution(student_msgs),
            "points": entry["points"],
        }
        if remark:
            record["teacher_remark"] = remark
        examples_out[sid] = record

    example_ids = set(examples_raw.keys())
    to_eval_out = {}
    for sid, entry in valid.items():
        if sid in example_ids:
            continue
        msgs = entry["msgs"]
        student_msgs = [m for m in msgs if not m["is_teacher"]]
        to_eval_out[sid] = {"solution": build_solution(student_msgs)}

    return examples_out, to_eval_out


def main():
    rng = random.Random(SEED)
    EXAMPLES_DIR.mkdir(exist_ok=True)
    TO_EVAL_DIR.mkdir(exist_ok=True)

    problem_files = sorted(PROBLEMS_DIR.glob("*.json"))
    if not problem_files:
        print(f"No JSON files found in {PROBLEMS_DIR}")
        return

    total_examples = 0
    total_to_eval = 0

    for path in problem_files:
        examples_data, to_eval_data = process_problem(path, rng)
        name = path.name

        with open(EXAMPLES_DIR / name, "w") as f:
            json.dump(examples_data, f, ensure_ascii=False, indent=2)

        with open(TO_EVAL_DIR / name, "w") as f:
            json.dump(to_eval_data, f, ensure_ascii=False, indent=2)

        print(f"{name}: examples={len(examples_data)}, to_eval={len(to_eval_data)}")
        total_examples += len(examples_data)
        total_to_eval += len(to_eval_data)

    print(f"\nTotal: {total_examples} examples, {total_to_eval} to_eval")


if __name__ == "__main__":
    main()
