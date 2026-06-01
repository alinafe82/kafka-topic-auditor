from datetime import UTC, datetime, timedelta

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
    assert any(f.topic == "payments" and f.category == "stale" for f in rep.findings)


def test_generate_report_uses_single_audit_time():
    now = datetime(2026, 1, 30, 12, 0, 0, tzinfo=UTC)

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


def test_generate_report_rejects_naive_audit_time():
    with pytest.raises(ValueError, match="timezone-aware"):
        generate_report(KafkaClient(), now=datetime(2026, 1, 30, 12, 0, 0))


def test_generate_report_rejects_invalid_offsets():
    class BadOffsetClient(KafkaClient):
        def list_topics(self):
            return ["orders"]

        def get_offsets(self, topic):
            return (10, 5)

    with pytest.raises(ValueError, match="invalid offsets"):
        generate_report(BadOffsetClient())


def test_generate_report_rejects_naive_last_consumption_time():
    class NaiveTimestampClient(KafkaClient):
        def list_topics(self):
            return ["orders"]

        def last_consume_at(self, topic):
            return datetime(2026, 1, 1, 12, 0, 0)

    with pytest.raises(ValueError, match="timezone-aware"):
        generate_report(
            NaiveTimestampClient(),
            now=datetime(2026, 1, 30, 12, 0, 0, tzinfo=UTC),
        )


def test_cli_emits_json_report():
    runner = CliRunner()

    result = runner.invoke(main, ["--format", "json"])

    assert result.exit_code == 0
    assert '"empty_topics"' in result.output
    assert '"stale_topics"' in result.output


def test_library_exposes_no_delete_shaped_method():
    """The auditor produces review evidence. Adding a delete-shaped method
    would change the contract and is intentionally blocked at test time."""
    import auditor.client
    import auditor.report

    forbidden = ("delete", "remove", "drop", "purge", "destroy")
    for module in (auditor.client, auditor.report):
        for name in dir(module):
            if name.startswith("_"):
                continue
            lower = name.lower()
            assert not any(token in lower for token in forbidden), (
                f"{module.__name__}.{name} looks like a delete API. "
                f"This tool produces audit evidence, not destructive actions."
            )

    for name in dir(auditor.client.KafkaClient):
        if name.startswith("_"):
            continue
        lower = name.lower()
        assert not any(token in lower for token in forbidden), (
            f"KafkaClient.{name} looks like a delete API."
        )
