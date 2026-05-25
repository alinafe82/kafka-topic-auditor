from datetime import UTC, datetime
from typing import Optional

from .client import KafkaClient
from .models import TopicFinding, TopicReport


def generate_report(
    client: KafkaClient,
    stale_days: int = 28,
    now: Optional[datetime] = None,
) -> TopicReport:
    if stale_days < 1:
        raise ValueError("stale_days must be at least 1")

    topics = client.list_topics()
    audit_time = now or datetime.now(UTC)
    if audit_time.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    empty, stale, internal = [], [], []
    findings: list[TopicFinding] = []
    for t in topics:
        if client.is_internal(t):
            internal.append(t)
            findings.append(
                TopicFinding(
                    topic=t,
                    category="internal",
                    reason="topic matches an internal Kafka/platform prefix",
                )
            )
            continue
        min_off, max_off = client.get_offsets(t)
        if max_off < min_off:
            raise ValueError(f"invalid offsets for {t}: max offset is below min offset")
        if max_off - min_off == 0:
            empty.append(t)
            findings.append(
                TopicFinding(
                    topic=t,
                    category="empty",
                    reason=f"offset range is empty ({min_off}..{max_off})",
                )
            )
        last = client.last_consume_at(t)
        if last.tzinfo is None:
            raise ValueError(f"last consumption timestamp for {t} must be timezone-aware")
        age_days = (audit_time - last).days
        if age_days >= stale_days:
            stale.append(t)
            findings.append(
                TopicFinding(
                    topic=t,
                    category="stale",
                    reason=f"last consumption was {age_days} days ago",
                )
            )
    return TopicReport(
        empty_topics=empty,
        stale_topics=stale,
        ignored_internal=internal,
        generated_at=audit_time.isoformat(),
        findings=findings,
    )
