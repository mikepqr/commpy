import itertools
from collections.abc import Iterable
from pathlib import Path
from typing import Callable, Generator, Optional, TypeVar

import typer

app = typer.Typer(add_completion=False)


def _sorted_iter(seq: Iterable[str]) -> Generator[str, None, None]:
    """
    Yield items from a sorted sequence

    Raises ValueError if the sequence is found to be unsorted.
    """
    it = iter(seq)
    prev = next(it)
    yield prev
    for item in it:
        if item < prev:
            raise ValueError("Sequence is not sorted")
        yield item


T = TypeVar("T")


def _identity(x: T) -> T:
    return x


def comm(
    seq1: Iterable[str], seq2: Iterable[str], comptrans: Optional[Callable] = None
) -> Generator[tuple[str, int], None, None]:
    it1, it2 = _sorted_iter(seq1), _sorted_iter(seq2)

    if not seq1:
        yield from zip(it2, itertools.repeat(2))
        return
    if not seq2:
        yield from zip(it1, itertools.repeat(1))
        return

    if comptrans is None:
        comptrans = _identity

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
                yield (d1, 1)
                yield from zip(it1, itertools.repeat(1))
                break
        elif d1trans < d2trans:
            yield (d1, 1)
            try:
                d1 = next(it1)
            except StopIteration:
                yield (d2, 2)
                yield from zip(it2, itertools.repeat(2))
                break
        else:
            yield (d2, 2)
            try:
                d2 = next(it2)
            except StopIteration:
                yield (d1, 1)
                yield from zip(it1, itertools.repeat(1))
                break


@app.command()
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
            print(s, end="")
        elif hide1 or hide2:
            print(f"\t{s}", end="")
        else:
            print(f"\t\t{s}", end="")

    prints = {1: printcol1, 2: printcol2, 3: printcol3}

    comptrans = (lambda s: s.lower()) if ignorecase else None

    with open(file1) as lines1, open(file2) as lines2:
        for item, column in comm(lines1, lines2, comptrans=comptrans):
            prints[column](item)
