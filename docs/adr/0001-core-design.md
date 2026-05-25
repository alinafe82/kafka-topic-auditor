# ADR 0001: Keep Topic Cleanup Read-Only First

## Context

Kafka topic cleanup is risky because deleting a topic can remove data that a dormant service
still needs. The public repo should show the evidence-gathering path without implementing
destructive automation.

## Decision

Build a read-only auditor with a small Kafka client boundary, deterministic classification
logic, and JSON/table output.

## Alternatives Considered

- Add topic deletion support.
- Build a web dashboard.
- Couple the implementation directly to one Kafka client library.

## Why This Design Was Selected

I chose this design because cleanup automation should begin with evidence. A replaceable client
keeps Kafka authentication and broker details out of the core logic.

## Tradeoffs

The tradeoff is that the repo cannot prove behavior against a real cluster yet. It can prove
the classification rules and show where a real adapter belongs.

## Consequences

- The demo runs without credentials.
- The report can feed a later approval process.
- Destructive behavior remains intentionally absent.

## What Would Change At Larger Scale

At larger scale, I would add a real Kafka adapter, owner lookup, partition-level evidence,
approval tracking, and contract tests against a disposable Kafka environment. I would still keep
deletion outside the first version.
