import click
import os
from pprint import pprint


def extra_list(file_path, extract_type):
    data = []
    assert extract_type in ("isfile", "isdir")
    for f in os.listdir(file_path):
        absolute_file_path = os.path.join(file_path, f)
        if getattr(os.path, extract_type)(absolute_file_path):
            data.append(absolute_file_path)
    return data


def scanner(file_path):
    files = extra_list(file_path, "isfile")
    dirs = extra_list(file_path, "isdir")
    for f in files:
        yield f
    for d in dirs:
        yield from scanner(d)


@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    pprint(list(scanner(fpath)))


if __name__ == "__main__":
    main()
