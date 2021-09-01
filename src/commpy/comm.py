import itertools
from collections.abc import Iterable
from pathlib import Path
from typing import Callable, Optional

import typer


def comm(seq1: Iterable, seq2: Iterable, comptrans: Optional[Callable] = None):
    if comptrans is None:

        def _identity(x):
            return x

        comptrans = _identity

    it1, it2 = iter(seq1), iter(seq2)
    d1 = next(it1)
    d2 = next(it2)

    while True:
        d1trans, d2trans = comptrans(d1), comptrans(d2)
        if d1trans == d2trans:
            yield (d1, 3)
            try:
                d1 = next(it1)
            except StopIteration:
                yield from zip(it2, itertools.repeat(2))
                break
            try:
                d2 = next(it2)
            except StopIteration:
                yield from zip(it1, itertools.repeat(1))
                break
        elif d1trans < d2trans:
            yield (d1, 1)
            try:
                d1 = next(it1)
            except StopIteration:
                yield from zip(it2, itertools.repeat(2))
                break
        else:
            yield (d2, 2)
            try:
                d2 = next(it2)
            except StopIteration:
                yield from zip(it1, itertools.repeat(1))
                break


def cli(
    file1: Path,
    file2: Path,
    hide1: bool = typer.Option(False, "-1", help="Suppress printing of column 1"),
    hide2: bool = typer.Option(False, "-2", help="Suppress printing of column 2"),
    hide3: bool = typer.Option(False, "-3", help="Suppress printing of column 3"),
    ignorecase: bool = typer.Option(
        False, "-i", help="Case insensitive comparison of lines (not implemented)"
    ),
) -> None:
    def printcol1(s: str) -> None:
        if hide1:
            return
        else:
            print(s, end="")

    def printcol2(s: str) -> None:
        if hide2:
            return
        elif hide1:
            print(s, end="")
        else:
            print(f"\t{s}", end="")

    def printcol3(s: str) -> None:
        if hide3:
            return
        elif hide1 and hide2:
            print(s)
        elif hide1 or hide2:
            print(f"\t{s}", end="")
        else:
            print(f"\t\t{s}", end="")

    prints = {1: printcol1, 2: printcol2, 3: printcol3}

    comptrans = (lambda s: s.lower()) if ignorecase else None

    with open(file1) as lines1, open(file2) as lines2:
        for item, column in comm(lines1, lines2, comptrans=comptrans):
            prints[column](item)


def main():
    app = typer.Typer(add_completion=False)
    app.command()(cli)
    app()
