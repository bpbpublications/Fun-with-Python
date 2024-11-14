import click
import logging
import threading
import time


class VirusScanner:
    def __init__(self):
        self.threads = []

    def analyze(self, fpath):

        th = threading.Thread(target=self.analyze_path, args=(fpath,))
        self.threads.append(th)
        th = threading.Thread(target=self.analyze_locks)
        self.threads.append(th)

        for x in self.threads:
            x.start()

        for thread in self.threads:
            thread.join()

    def analyze_path(self, fpath):
        # code for analyzing
        for i in range(0, 5):
            print(f"analyze_path [{i}]")
            time.sleep(1)
        print(f"Finished analyzing path: {fpath}")

    def analyze_locks(self):
        for i in range(0, 10):
            print(f"analyze_locks [{i}]")
            time.sleep(0.8)
        print(f"Finished creating and analyzing locks")


@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    v = VirusScanner()
    v.analyze(fpath)


if __name__ == "__main__":
    main()
