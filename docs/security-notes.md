# Security Notes

## Threat Assumptions

- The local demo uses a mock Kafka client and requires no broker credentials.
- In a real deployment, Kafka credentials and broker endpoints would be provided outside the
  repository.
- The tool is intended to report cleanup candidates, not mutate Kafka.

## What It Protects Against

- Accidental inspection of internal Kafka topics by skipping known internal prefixes before
  offset lookups.
- Unsafe automatic deletion by not implementing destructive operations.
- Invalid stale thresholds.
- Secret commits through CI secret scanning and local pre-commit guidance.

## What It Does Not Protect Against

- Compromised Kafka credentials in a future real adapter.
- Incorrect topic ownership metadata.
- False positives when consumer groups are inactive for a valid reason.
- Data loss if a future deletion command is added without approval gates.

## Safe Local Usage

```bash
uv run python -m auditor.cli --format json
```

Do not commit broker URLs, SASL passwords, TLS keys, or private topic names from an employer
environment.

## Known Limitations

The current implementation is read-only and mocked. A real adapter should use least-privilege
Kafka credentials and should emit evidence rather than perform deletion.
