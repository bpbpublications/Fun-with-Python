import click
import os


def scanner(file_path):
    for (root, dirs, files) in os.walk(file_path, topdown=True):
        for f in files:
            yield os.path.join(root, f)


@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    scanner(fpath)


if __name__ == "__main__":
    main()
