# Production Readiness

## Current State

What works:

- The report logic classifies topics as empty, stale, or ignored internal topics.
- The CLI emits table or JSON output.
- Internal topics are skipped before offset or consumption lookup.
- Unit tests cover classification, boundary timing, invalid thresholds, internal-topic skips,
  and JSON CLI output.
- CI runs tests, linting, and secret scanning.

What is broken:

- Nothing known in the local mock workflow.

What is unclear:

- The mock client does not represent real Kafka authentication, partition offsets, or owner
  metadata.

What is missing:

- A real Kafka Admin and consumer-group adapter.
- Evidence fields such as partition-level offsets, topic owner, retention policy, and last
  producer activity.
- An approval workflow before deletion.

What is risky:

- Any future deletion command would be high risk unless it is gated by dry-run output, evidence,
  and owner approval.

## Readiness Scores

| Area | Before | Current | Notes |
| --- | ---: | ---: | --- |
| correctness | 6 | 7 | Classification is deterministic; real Kafka data is not wired in. |
| test coverage | 5 | 8 | Core cases, boundary dates, CLI JSON, and internal skips are tested. |
| architecture clarity | 7 | 8 | Client/report/model/CLI boundaries are clear. |
| maintainability | 7 | 8 | Small functions with explicit behavior. |
| security | 7 | 8 | Read-only by design; no secret requirement for local use. |
| dependency hygiene | 6 | 8 | Missing Click dependency was fixed; dependency set remains small. |
| configuration | 5 | 6 | CLI threshold is configurable; real broker config is out of scope. |
| error handling | 5 | 7 | Invalid stale threshold is rejected. |
| logging | 4 | 5 | Output is quiet and reviewer-friendly; no operational logs yet. |
| observability | 4 | 5 | JSON output can feed later automation. |
| documentation | 6 | 8 | Architecture, runbook, security, ADR, and interview notes are present. |
| CI/CD | 6 | 8 | CI runs lint, tests, and secret scanning. |
| local developer experience | 6 | 8 | Quickstart and CLI run without Kafka. |

## Top Issues Blocking Interview Readiness

P0:

- None known for the public demo path.

P1:

- The Kafka adapter is mocked.
- The report lacks owner/evidence metadata a real cleanup process would need.

P2:

- Add contract tests once a real adapter exists.
- Add report export to a file when the output becomes part of an approval workflow.

## Recommended Productionization Path

Keep the current repo as a read-only auditor. The next practical step is a real adapter that
collects metadata without deleting anything. Deletion should remain out of scope until the tool
can produce reviewable evidence and require owner approval.
