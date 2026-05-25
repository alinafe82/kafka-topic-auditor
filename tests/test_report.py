from datetime import datetime, timedelta

from auditor.client import KafkaClient
from auditor.report import generate_report


def test_generate_report():
    rep = generate_report(KafkaClient(), stale_days=28)
    assert "dead-letter" in rep.empty_topics
    assert "payments" in rep.stale_topics
    assert "__consumer_offsets" in rep.ignored_internal


def test_generate_report_uses_single_audit_time():
    now = datetime(2026, 1, 30, 12, 0, 0)

    class BoundaryClient(KafkaClient):
        def list_topics(self):
            return ["boundary"]

        def get_offsets(self, topic):
            return (0, 10)

        def last_consume_at(self, topic):
            return now - timedelta(days=28)

    rep = generate_report(BoundaryClient(), stale_days=28, now=now)

    assert rep.stale_topics == ["boundary"]
    assert rep.generated_at == now.isoformat()
