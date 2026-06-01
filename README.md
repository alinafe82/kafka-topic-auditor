# kafka-topic-auditor

A Kafka topic-hygiene tool that produces a reviewable list of cleanup candidates. Empty topics, topics that have not been consumed in N days, and internal platform topics are each handled with the right behaviour and reason attached.

The tool never deletes anything. It produces evidence. Whoever decides to delete a topic does that from a separate workflow with the audit output as the input.

## Topic hygiene as platform risk

The cost of leaving a stale topic alone is low. The cost of deleting a topic that one team forgot they were still consuming from is high. So the right interface is not "find unused topics and delete them"; the right interface is "surface candidates with the reason, and let a human approve."

That framing decides the rest of the design:

- the report includes the reason for every flag, not a binary decision.
- internal topics (`__consumer_offsets`, `_schema`, `_confluent`, `__transaction_state`) are reported separately so a reviewer can confirm they were not even considered for deletion.
- the audit timestamp is part of the report. Staleness is a function of "now", and "now" is recorded.
- there is no delete code path in the library. Removing the delete API surface removes the failure mode where a bug or a misclick wipes a topic.

## Delete safety

- The tool has no delete operation. There is no `--apply`, no `--yes`, no `delete_topics` call. A test asserts that the library exposes no method whose name implies deletion.
- The output is JSON or a terminal table. Both formats include the reason for every flag.
- The recommended workflow is: run the audit, attach the JSON to a ticket, get an owner sign-off, then delete from a separate runbook. The audit JSON is the artefact that survives the deletion.
- If you wire this into automation later, the right place to add the delete call is in the runbook, not in the auditor.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m auditor.cli --format table
python -m auditor.cli --format json
```

With `uv`:

```bash
uv run --extra dev pytest
uv run --extra dev ruff check .
```

## How the audit pass runs

- `auditor.client.KafkaClient` is the local deterministic adapter so the repo can be reviewed without a Kafka cluster. A real adapter would wrap the Kafka Admin API and consumer-group offset lookups; the interface stays the same.
- `auditor.report.generate_report` walks each topic, classifies it, attaches a reason, and returns a `TopicReport`. Internal topics are recognised before any expensive offset lookup, which the tests enforce.
- `auditor.cli` turns the report into JSON or a terminal table. Nothing else.

Design notes: [docs/architecture.md](docs/architecture.md). Operator flow: [docs/runbook.md](docs/runbook.md).

## What the tests prove

- internal topics are skipped before any offset lookup (the test client raises if offsets are requested for an internal topic).
- empty topics (no min/max offset gap) are flagged as `empty`.
- topics with no consumption in `stale_days` days are flagged as `stale`.
- the audit timestamp is timezone-aware and required to be timezone-aware.
- inverted offset metadata (`max < min`) is rejected with a clear error.
- the JSON output contract includes the `empty_topics` and `stale_topics` arrays.
- the library exposes no delete-shaped method.

## Adapter work left before this would run against a real Kafka cluster

- A Kafka Admin API adapter implementing `list_topics`, `is_internal`, `get_offsets`, and `last_consume_at`.
- Per-partition offset and retention metadata so the empty-topic check is not fooled by a recently compacted topic.
- A machine-readable evidence file format the deletion runbook can consume.

## Operational notes

- [docs/runbook.md](docs/runbook.md)
- [docs/security-notes.md](docs/security-notes.md)
- [docs/production-readiness.md](docs/production-readiness.md)
- [docs/interview-notes.md](docs/interview-notes.md)
