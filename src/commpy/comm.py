import sys
from pathlib import Path

import typer


class Merger:
    def __init__(
        self,
        lines1,
        lines2,
        hide1: bool = False,
        hide2: bool = False,
        hide3: bool = False,
        ignorecase: bool = False,
    ):
        self.lines1, self.lines2 = lines1, lines2
        self.hide1, self.hide2, self.hide3 = hide1, hide2, hide3
        if ignorecase:
            raise NotImplementedError

    def printcol1(self, s):
        if self.hide1:
            return
        else:
            print(s)

    def printcol2(self, s):
        if self.hide2:
            return
        elif self.hide1:
            print(s)
        else:
            print(f"\t{s}")

    def printcol3(self, s):
        if self.hide3:
            return
        elif self.hide1 and self.hide2:
            print(s)
        elif self.hide1 or self.hide2:
            print(f"\t{s}")
        else:
            print(f"\t\t{s}")

    def next_maybe_flush(self, it1, it2, flusher=print):
        try:
            return next(it1).strip()
        except StopIteration:
            self.flush(it2, flusher=flusher)

    def flush(self, it, flusher=print):
        for item in it:
            flusher(item)
        sys.exit(0)

    def merge(self):
        d1 = self.next_maybe_flush(self.lines1, self.lines2)
        d2 = self.next_maybe_flush(self.lines2, self.lines1)

        while True:
            if d1 == d2:
                self.printcol3(d1)
                d1 = self.next_maybe_flush(
                    self.lines1, self.lines2, flusher=self.printcol2
                )
                d2 = self.next_maybe_flush(
                    self.lines2, self.lines1, flusher=self.printcol1
                )
            elif d1 < d2:
                self.printcol1(d1)
                d1 = self.next_maybe_flush(
                    self.lines1, self.lines2, flusher=self.printcol2
                )
            else:
                self.printcol2(d2)
                d2 = self.next_maybe_flush(
                    self.lines2, self.lines1, flusher=self.printcol1
                )


def comm(
    file1: Path,
    file2: Path,
    hide1: bool = typer.Option(False, "-1", help="Suppress printing of column 1"),
    hide2: bool = typer.Option(False, "-2", help="Suppress printing of column 2"),
    hide3: bool = typer.Option(False, "-3", help="Suppress printing of column 3"),
    ignorecase: bool = typer.Option(
        False, "-i", help="Case insensitive comparison of lines (not implemented)"
    ),
):
    with open(file1) as lines1, open(file2) as lines2:
        m = Merger(
            lines1,
            lines2,
            hide1=hide1,
            hide2=hide2,
            hide3=hide3,
            ignorecase=ignorecase,
        )
        m.merge()


def main():
    typer.run(comm)
