#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const evaluatedDir = path.join(scriptDir, "evaluated");
const exportDir = path.join(evaluatedDir, "export");
const markdownDir = path.join(exportDir, "markdown");
const scoreValues = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4];

function compareHomeworkFiles(a, b) {
  const [, aHomework, aPart] = a.match(/^du(\d+)_(\d+)\.json$/).map(Number);
  const [, bHomework, bPart] = b.match(/^du(\d+)_(\d+)\.json$/).map(Number);
  return aHomework - bHomework || aPart - bPart;
}

function compareStudentIds(a, b) {
  const aNumber = Number(a);
  const bNumber = Number(b);
  if (Number.isFinite(aNumber) && Number.isFinite(bNumber)) {
    return aNumber - bNumber;
  }
  return a.localeCompare(b, "en", { numeric: true });
}

function homeworkInfo(filename) {
  const match = filename.match(/^du(\d+)_(\d+)\.json$/);
  if (!match) {
    throw new Error(`Unexpected evaluation filename: ${filename}`);
  }
  const [, homework, part] = match;
  return {
    key: filename.replace(/\.json$/, ""),
    label: `DU ${homework}.${part}`,
  };
}

function csvCell(value) {
  const text = value === null || value === undefined ? "" : String(value);
  return `"${text.replaceAll('"', '""')}"`;
}

function makeCsv(rows) {
  return `${rows.map((row) => row.map(csvCell).join(",")).join("\r\n")}\r\n`;
}

function formatNumber(value, maximumFractionDigits = 3) {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits,
    minimumFractionDigits: 0,
  }).format(value);
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const midpoint = Math.floor(sorted.length / 2);
  return sorted.length % 2
    ? sorted[midpoint]
    : (sorted[midpoint - 1] + sorted[midpoint]) / 2;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function htmlParagraph(value) {
  return `<p>${escapeHtml(value).replaceAll("\n", "<br>\n")}</p>`;
}

function summarize(records) {
  const points = records.map((record) => record.points);
  const scoreCounts = Object.fromEntries(scoreValues.map((score) => [score, 0]));
  for (const pointValue of points) {
    scoreCounts[pointValue] = (scoreCounts[pointValue] ?? 0) + 1;
  }
  const correct = records.filter((record) => record.correct).length;
  return {
    submissions: records.length,
    average: points.reduce((total, value) => total + value, 0) / points.length,
    median: median(points),
    correct,
    incorrect: records.length - correct,
    correctRate: (correct / records.length) * 100,
    scoreCounts,
  };
}

function homeworkMarkdown(homework, summary) {
  const distributionRows = scoreValues
    .map((score) => `| ${score} | ${summary.scoreCounts[score]} |`)
    .join("\n");
  const studentSections = homework.records
    .map((record) => {
      const status = record.correct ? "✅ correct" : "⚠️ needs revision";
      return [
        "<details>",
        `<summary><strong>Student ${escapeHtml(record.studentId)}</strong> — ${record.points}/4 — ${status}</summary>`,
        "",
        "#### Zpětná vazba pro studenta",
        "",
        htmlParagraph(record.feedback),
        "",
        "<details>",
        "<summary>Evaluator justification (English)</summary>",
        "",
        htmlParagraph(record.justification),
        "",
        "</details>",
        "",
        "</details>",
      ].join("\n");
    })
    .join("\n\n");

  return [
    `# ${homework.label} evaluations`,
    "",
    "[← Evaluation dashboard](../README.md) · [Combined CSV](../all_evaluations.csv)",
    "",
    "> Student feedback is shown separately from the evaluator-only justification. Expand a student row to view the evaluation; the justification has its own nested disclosure.",
    "",
    "## Overview",
    "",
    "| Metric | Value |",
    "| --- | ---: |",
    `| Submissions | ${summary.submissions} |`,
    `| Average score | ${formatNumber(summary.average)} / 4 |`,
    `| Median score | ${formatNumber(summary.median)} / 4 |`,
    `| Fully correct | ${summary.correct} (${formatNumber(summary.correctRate, 1)}%) |`,
    `| Below full credit | ${summary.incorrect} |`,
    "",
    "## Score distribution",
    "",
    "| Points | Students |",
    "| ---: | ---: |",
    distributionRows,
    "",
    "## Individual evaluations",
    "",
    studentSections,
    "",
  ].join("\n");
}

const evaluationFiles = fs
  .readdirSync(evaluatedDir)
  .filter((filename) => /^du\d+_\d+\.json$/.test(filename))
  .sort(compareHomeworkFiles);

if (evaluationFiles.length === 0) {
  throw new Error(`No evaluation JSON files found in ${evaluatedDir}`);
}

const homeworks = evaluationFiles.map((filename) => {
  const info = homeworkInfo(filename);
  const source = JSON.parse(fs.readFileSync(path.join(evaluatedDir, filename), "utf8"));
  const records = Object.entries(source)
    .sort(([a], [b]) => compareStudentIds(a, b))
    .map(([studentId, evaluation]) => ({ studentId, ...evaluation }));

  for (const record of records) {
    for (const field of ["points", "correct", "justification", "feedback"]) {
      if (!(field in record)) {
        throw new Error(`${filename}, student ${record.studentId}: missing ${field}`);
      }
    }
  }

  return { filename, ...info, records };
});

const summaries = homeworks.map((homework) => ({
  ...homework,
  summary: summarize(homework.records),
}));
const allRecords = homeworks.flatMap((homework) =>
  homework.records.map((record) => ({ ...record, homework: homework.key })),
);
const overall = summarize(allRecords);

fs.mkdirSync(markdownDir, { recursive: true });

const evaluationCsvRows = [
  ["homework", "student_id", "points", "correct", "feedback", "justification"],
  ...allRecords.map((record) => [
    record.homework,
    record.studentId,
    record.points,
    record.correct,
    record.feedback,
    record.justification,
  ]),
];
fs.writeFileSync(
  path.join(exportDir, "all_evaluations.csv"),
  makeCsv(evaluationCsvRows),
  "utf8",
);

const scoreHeaders = scoreValues.map((score) => `score_${String(score).replace(".", "_")}`);
const summaryCsvRows = [
  [
    "homework",
    "submissions",
    "average_points",
    "median_points",
    "fully_correct",
    "below_full_credit",
    "fully_correct_percent",
    ...scoreHeaders,
  ],
  ...summaries.map(({ key, summary }) => [
    key,
    summary.submissions,
    summary.average.toFixed(3),
    summary.median,
    summary.correct,
    summary.incorrect,
    summary.correctRate.toFixed(1),
    ...scoreValues.map((score) => summary.scoreCounts[score]),
  ]),
  [
    "ALL",
    overall.submissions,
    overall.average.toFixed(3),
    overall.median,
    overall.correct,
    overall.incorrect,
    overall.correctRate.toFixed(1),
    ...scoreValues.map((score) => overall.scoreCounts[score]),
  ],
];
fs.writeFileSync(
  path.join(exportDir, "homework_summary.csv"),
  makeCsv(summaryCsvRows),
  "utf8",
);

for (const homework of summaries) {
  fs.writeFileSync(
    path.join(markdownDir, `${homework.key}.md`),
    homeworkMarkdown(homework, homework.summary),
    "utf8",
  );
}

const dashboardRows = summaries
  .map(
    ({ key, label, summary }) =>
      `| [${label}](markdown/${key}.md) | ${summary.submissions} | ${formatNumber(summary.average)} | ${formatNumber(summary.median)} | ${summary.correct} | ${formatNumber(summary.correctRate, 1)}% |`,
  )
  .join("\n");
const overallDistribution = scoreValues
  .map((score) => `| ${score} | ${overall.scoreCounts[score]} |`)
  .join("\n");
const dashboard = [
  "# Homework evaluation dashboard",
  "",
  `This export contains **${overall.submissions.toLocaleString("en-US")} evaluations** across **${homeworks.length} homework parts**.`,
  "",
  "## Downloads",
  "",
  "- [All individual evaluations (CSV)](all_evaluations.csv)",
  "- [Homework-level summary (CSV)](homework_summary.csv)",
  "",
  "Both files use UTF-8 encoding and comma-separated, double-quoted fields. The combined CSV keeps student-facing `feedback` separate from evaluator-only `justification`.",
  "",
  "## Homework overview",
  "",
  "| Homework | Submissions | Average / 4 | Median / 4 | Fully correct | Full-credit rate |",
  "| --- | ---: | ---: | ---: | ---: | ---: |",
  dashboardRows,
  `| **Overall** | **${overall.submissions}** | **${formatNumber(overall.average)}** | **${formatNumber(overall.median)}** | **${overall.correct}** | **${formatNumber(overall.correctRate, 1)}%** |`,
  "",
  "## Overall score distribution",
  "",
  "| Points | Students |",
  "| ---: | ---: |",
  overallDistribution,
  "",
  "## Presentation notes",
  "",
  "Each homework link opens a web-friendly Markdown page. Individual student rows are collapsible, and the evaluator-only justification is placed in a separate nested disclosure beneath the Czech student feedback.",
  "",
  "The files are generated from the evaluation JSON files by running:",
  "",
  "```bash",
  "node ../export_evaluations.mjs",
  "```",
  "",
].join("\n");
fs.writeFileSync(path.join(exportDir, "README.md"), dashboard, "utf8");

console.log(
  `Exported ${overall.submissions} evaluations from ${homeworks.length} homework files to ${exportDir}`,
);
