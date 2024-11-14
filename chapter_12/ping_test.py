import click
from ping3 import ping


def ping_host(host):
    result = ping(host)
    click.echo(f"Response time {result}s")


@click.command()
@click.option("--host", help="Host to ping")
def main(host):
    ping_host(host)


if __name__ == "__main__":
    main()
