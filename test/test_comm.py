import pytest

from commpy.comm import comm


def test_abcd():
    assert tuple(comm(list("abc"), list("bcd"))) == (
        ("a", 1),
        ("b", 3),
        ("c", 3),
        ("d", 2),
    )


def test_case():
    assert tuple(comm(list("abc"), list("Bcd"))) == (
        ("B", 2),
        ("a", 1),
        ("b", 1),
        ("c", 3),
        ("d", 2),
    )


def test_ignorecase():
    assert tuple(comm(list("abc"), list("Bcd"), comptrans=lambda s: s.lower())) == (
        ("a", 1),
        ("b", 3),
        ("c", 3),
        ("d", 2),
    )


def test_empty():
    assert tuple(comm(list("abc"), [])) == (
        ("a", 1),
        ("b", 1),
        ("c", 1),
    )


def test_unsorted():
    with pytest.raises(ValueError):
        _ = tuple(comm(list("abc"), list("cdb")))
