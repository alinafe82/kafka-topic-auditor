# Interview Notes

## 60-Second Explanation

This is a Python CLI for Kafka topic hygiene. It reads topic metadata through a small client
interface, ignores internal topics, flags empty topics, and flags topics with no recent
consumption. It returns a report rather than deleting anything.

## Decisions I Can Defend

- Reporting candidates is safer than automating deletion immediately.
- The Kafka client is a replaceable adapter because cluster auth and metadata conventions vary.
- Classification logic is kept outside the CLI so it can be tested and reused.

## Tradeoffs

The current implementation uses a mock client and simplified offsets. That makes the repo safe
to run locally but means production use needs a real adapter and stronger ownership metadata.

## Fixes Made During Portfolio Hardening

- Declared dev tooling for fresh-clone tests.
- Added deterministic timing support to report generation.
- Added a license, architecture notes, ADR, and interview notes.

## Fixes Made During Productionization

- Fixed the missing Click dependency so the documented CLI works from a fresh install.
- Added tests for internal-topic skips, invalid stale thresholds, and JSON CLI output.
- Added production-readiness, security, runbook, and core design ADR docs.
- Updated CI to run ruff as well as tests.

## Likely Questions

**Why not delete topics automatically?**
Because topic deletion can break producers, consumers, audits, or incident response. I would
first produce evidence, route it to owners, and require approval.

**What would you add for production?**
A real Kafka Admin adapter, owner lookup, exclusions, audit logs, and an approval workflow.

**What does this show for Engineering Productivity?**
It shows practical automation that reduces operational toil while respecting safety boundaries.
