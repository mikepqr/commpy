import pytest

from commpy.comm import comm


def test_abcd():
    assert tuple(comm(list("abc"), list("bcd"))) == (
        ("a", 1),
        ("b", 3),
        ("c", 3),
        ("d", 2),
    )


def test_abcd_reversed():
    assert tuple(comm(list("bcd"), list("abc"))) == (
        ("a", 2),
        ("b", 3),
        ("c", 3),
        ("d", 1),
    )


def test_length():
    assert tuple(comm(list("abc"), list("a"))) == (
        ("a", 3),
        ("b", 1),
        ("c", 1),
    )


def test_d1_lessthan_d2_flush():
    assert tuple(comm(list("a"), list("bcd"))) == (
        ("a", 1),
        ("b", 2),
        ("c", 2),
        ("d", 2),
    )


def test_d2_lessthan_d1_flush():
    assert tuple(comm(list("bcd"), list("a"))) == (
        ("a", 2),
        ("b", 1),
        ("c", 1),
        ("d", 1),
    )


def test_length_reversed():
    assert tuple(comm(list("a"), list("abc"))) == (
        ("a", 3),
        ("b", 2),
        ("c", 2),
    )


def test_casesensitive():
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


def test_empty_reversed():
    assert tuple(comm([], list("abc"))) == (
        ("a", 2),
        ("b", 2),
        ("c", 2),
    )


def test_unsorted():
    with pytest.raises(ValueError):
        _ = tuple(comm(list("abc"), list("cdb")))
