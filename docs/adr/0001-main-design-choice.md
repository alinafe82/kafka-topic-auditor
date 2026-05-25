# ADR 0001: Report Cleanup Candidates Instead of Deleting Topics

## Status

Accepted

## Context

Topic deletion is destructive. A developer productivity tool should reduce manual review work
without turning a weak signal into an outage.

## Decision

The tool emits evidence-backed cleanup candidates and leaves deletion outside the repo.

## Consequences

This keeps the tool safe to run in read-only environments. The tradeoff is that cleanup still
requires a separate approval or execution workflow.
