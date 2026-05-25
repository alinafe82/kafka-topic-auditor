# kafka-topic-auditor
Audit Kafka topics for cleanup candidates.

The goal is to make topic hygiene reviewable before anyone deletes infrastructure. The CLI
flags topics that are empty, stale based on recent consumption, or ignored because they are
Kafka/internal platform topics.
JSON output includes per-topic findings with the reason each topic was flagged.

The current client is a local mock. A production version would replace `KafkaClient` with a
real adapter for Kafka Admin APIs and consumer group offsets.

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

## Architecture Overview

- `auditor.client` defines the Kafka-facing interface.
- `auditor.report` contains the topic classification logic.
- `auditor.models` defines the report contract.
- `auditor.cli` turns the report into JSON or a terminal table.

See [docs/architecture.md](docs/architecture.md) for design details.
See [docs/runbook.md](docs/runbook.md), [docs/security-notes.md](docs/security-notes.md),
and [docs/production-readiness.md](docs/production-readiness.md) for operational notes.

## Limitations

- The Kafka client is mocked.
- Offset checks are simplified across partitions.
- The tool reports candidates only; it does not delete topics.

## Future Improvements

- Add a real Kafka Admin client adapter.
- Include per-partition offset and retention metadata.
- Emit machine-readable evidence for an approval workflow.

## Interview Notes

See [docs/interview-notes.md](docs/interview-notes.md).
