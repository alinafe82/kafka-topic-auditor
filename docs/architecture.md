# Architecture

## Problem

Kafka clusters accumulate topics that no longer have producers or consumers. Deleting topics
without evidence is risky, but leaving abandoned topics makes ownership and operations harder.
This repo builds a small audit path that produces cleanup candidates without mutating the
cluster.

## Intended User

The intended user is a platform engineer or service owner preparing a topic cleanup review.

## Components

- `KafkaClient`: adapter boundary for topic names, offsets, and last-consumption timestamps.
- `generate_report`: classifies topics as empty, stale, or ignored internal topics.
- `TopicReport`: structured output with per-topic findings for CLI and future automation.
- CLI: renders the report as JSON or a terminal table.

## Data Flow

The CLI creates a client, `generate_report` reads topic metadata, internal topics are filtered
out, offsets identify empty topics, and last-consumption timestamps identify stale topics.
The output is a report with reasons, not an action.

## Design Choices

I kept deletion out of scope because cleanup automation should start with evidence and approval.
The report contract can later feed a ticket, Slack workflow, or pull request without changing
the classification logic.

The client is intentionally small. Real Kafka environments vary in authentication, broker
discovery, and consumer group conventions, so the adapter should be replaceable.

## What Is Not Built

This is not a Kafka admin console. It does not connect to brokers, delete topics, or infer
business ownership.

## Extension Points

- Replace the mock client with a real Kafka Admin implementation.
- Add owner lookup from tags, naming conventions, or service catalogs.
- Add an approval workflow before any destructive action.

## Operational Considerations

A production version should avoid deleting topics automatically. It should record evidence,
require owner approval, and support exclusions for regulated or incident-response topics.

## Testing Strategy

Tests cover classification logic and boundary timing. A real adapter should be tested with
contract tests against a disposable Kafka container.
