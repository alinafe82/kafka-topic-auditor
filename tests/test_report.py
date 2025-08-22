from auditor.client import KafkaClient
from auditor.report import generate_report

def test_generate_report():
    rep = generate_report(KafkaClient(), stale_days=28)
    assert "dead-letter" in rep.empty_topics
    assert "payments" in rep.stale_topics
    assert "__consumer_offsets" in rep.ignored_internal
