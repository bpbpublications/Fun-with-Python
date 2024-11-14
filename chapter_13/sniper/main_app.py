import click
from pprint import pprint
from clients.main import Main


@click.command()
@click.option("--order", help="Sorting order", type=click.Choice(["asc", "desc"], case_sensitive=False))
@click.option("--limit", type=int, help="Limit number of results", required=False)
@click.option("--phrase", type=str, help="Item name to look for", required=True)
def main(order, limit, phrase):
    m = Main()
    result = m.collect_results(phrase)
    if result:
        if order == "desc":
            result.sort(key=lambda x: float(x.get("price", 0)), reverse=True)
        if limit:
            result = result[:limit]
    pprint(result)


if __name__ == "__main__":
    main()
