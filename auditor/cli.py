import json

import click
from rich.console import Console
from rich.table import Table

from .client import KafkaClient
from .report import generate_report

console = Console()


@click.command()
@click.option("--stale-days", default=28, type=click.IntRange(1), show_default=True)
@click.option("--format", "fmt", type=click.Choice(["table", "json"]), default="table")
def main(stale_days: int, fmt: str) -> None:
    client = KafkaClient()
    rep = generate_report(client, stale_days=stale_days)
    if fmt == "json":
        console.print_json(data=json.loads(rep.model_dump_json()))
        return
    table = Table(title="Kafka Topic Audit")
    table.add_column("Empty Topics")
    table.add_column("Stale Topics")
    table.add_column("Ignored (Internal)")
    rows = max(len(rep.empty_topics), len(rep.stale_topics), len(rep.ignored_internal))
    for i in range(rows):
        table.add_row(
            rep.empty_topics[i] if i < len(rep.empty_topics) else "",
            rep.stale_topics[i] if i < len(rep.stale_topics) else "",
            rep.ignored_internal[i] if i < len(rep.ignored_internal) else "",
        )
    console.print(table)


if __name__ == "__main__":
    main()
