from datetime import datetime, timedelta

import pytest
from click.testing import CliRunner

from auditor.cli import main
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


def test_generate_report_skips_internal_topics_without_offset_lookup():
    class InternalOnlyClient(KafkaClient):
        def list_topics(self):
            return ["__consumer_offsets"]

        def get_offsets(self, topic):
            raise AssertionError("internal topics should not be inspected")

        def last_consume_at(self, topic):
            raise AssertionError("internal topics should not be inspected")

    rep = generate_report(InternalOnlyClient())

    assert rep.ignored_internal == ["__consumer_offsets"]
    assert rep.empty_topics == []
    assert rep.stale_topics == []


def test_generate_report_rejects_invalid_stale_days():
    with pytest.raises(ValueError, match="stale_days"):
        generate_report(KafkaClient(), stale_days=0)


def test_cli_emits_json_report():
    runner = CliRunner()

    result = runner.invoke(main, ["--format", "json"])

    assert result.exit_code == 0
    assert '"empty_topics"' in result.output
    assert '"stale_topics"' in result.output
