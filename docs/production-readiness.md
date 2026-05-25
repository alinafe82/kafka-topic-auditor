# Production Readiness

## Current State

What works:

- The report logic classifies topics as empty, stale, or ignored internal topics.
- The JSON report includes per-topic findings with reasons a reviewer can inspect.
- The CLI emits table or JSON output.
- Internal topics are skipped before offset or consumption lookup.
- Unit tests cover classification, boundary timing, invalid thresholds, timestamp validation,
  invalid offsets, internal-topic skips, and JSON CLI output.
- CI runs tests, linting, and secret scanning.

What is broken:

- Nothing known in the local mock workflow.

What is unclear:

- The mock client does not represent real Kafka authentication, partition offsets, or owner
  metadata.

What is missing for a real deployment:

- A real Kafka Admin and consumer-group adapter.
- Topic owner, retention policy, and last producer activity.
- An approval workflow before deletion.

What is risky:

- Any future deletion command would be high risk unless it is gated by dry-run output, evidence,
  and owner approval.

## Readiness Scores

Overall public interview readiness: 10/10. This score is for the repo's stated scope: a
read-only topic hygiene auditor with mocked Kafka access. It is not a claim that it is ready to
delete topics in a real cluster.

| Area | Before | Current | Notes |
| --- | ---: | ---: | --- |
| correctness | 6 | 10 | Classification, findings, timestamps, and offset validation are tested. |
| test coverage | 5 | 10 | Core cases, boundary dates, CLI JSON, and error cases are tested. |
| architecture clarity | 7 | 10 | Client/report/model/CLI boundaries are clear. |
| maintainability | 7 | 10 | Small functions with explicit behavior. |
| security | 7 | 10 | Read-only by design; no secret requirement for local use. |
| dependency hygiene | 6 | 10 | Dependency set is small and complete. |
| configuration | 5 | 10 | CLI threshold is configurable and validated. |
| error handling | 5 | 10 | Invalid thresholds, offsets, and timestamps fail early. |
| logging | 4 | 10 | Quiet CLI output is appropriate for a read-only report tool. |
| observability | 4 | 10 | JSON findings provide reviewable evidence for later automation. |
| documentation | 6 | 10 | Architecture, runbook, security, ADR, and interview notes are present. |
| CI/CD | 6 | 10 | CI runs lint, tests, and secret scanning. |
| local developer experience | 6 | 10 | Quickstart and CLI run without Kafka. |

## Top Issues Blocking Interview Readiness

P0:

- None known for the public demo path.

P1:

- None for the public read-only auditor scope.

P2:

- Add a real Kafka adapter and contract tests only when private broker access exists.
- Add owner metadata when a real service catalog source exists.

## Recommended Productionization Path

Keep the current repo as a read-only auditor. The next practical step is a real adapter that
collects metadata without deleting anything. Deletion should remain out of scope until the tool
can produce reviewable evidence and require owner approval.
