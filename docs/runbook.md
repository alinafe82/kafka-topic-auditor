# Runbook

## Run Locally

```bash
uv run python -m auditor.cli --format table
uv run python -m auditor.cli --format json
```

## Test

```bash
uv run --extra dev pytest
uv run --extra dev ruff check .
```

## Common Failure Modes

- Invalid `--stale-days`: use a positive integer.
- Missing `click`: install dependencies from `requirements.txt` or use `uv run --extra dev`.
- Unexpected stale topics: check the client implementation and the audit timestamp.

## Troubleshooting

- Use JSON output when comparing reports in tests or automation.
- Confirm internal-topic prefixes before adding a real Kafka adapter.
- Keep the report read-only until evidence and approval workflow are designed.

## Safe Cleanup

The local demo does not create Kafka resources or files. Remove `.venv`, `.pytest_cache`, or
`__pycache__` if needed.

## Known Limitations

The mock client does not represent partition-level offsets, topic ownership, or real consumer
group behavior.
