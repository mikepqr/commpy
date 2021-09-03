from pathlib import Path

import pytest
from typer.testing import CliRunner

from commpy.comm import app

runner = CliRunner()


@pytest.fixture
def f1(tmp_path: Path):
    f1 = tmp_path / "f1"
    f1.write_text("a\nb\nc\n")
    return str(f1)


@pytest.fixture
def f2(tmp_path: Path):
    f2 = tmp_path / "f2"
    f2.write_text("b\nc\nd\n")
    return str(f2)


def test_app(f1, f2):
    result = runner.invoke(app, [str(f1), str(f2)])
    expected_stdout = "a\n\t\tb\n\t\tc\n\td\n"
    assert result.stdout == expected_stdout


def test_hide1(f1, f2):
    result = runner.invoke(app, [str(f1), str(f2), "-1"])
    expected_stdout = "\tb\n\tc\nd\n"
    assert result.stdout == expected_stdout


def test_hide12(f1, f2):
    result = runner.invoke(app, [str(f1), str(f2), "-1", "-2"])
    expected_stdout = "b\nc\n"
    assert result.stdout == expected_stdout


def test_hide3(f1, f2):
    result = runner.invoke(app, [str(f1), str(f2), "-3"])
    expected_stdout = "a\n\td\n"
    assert result.stdout == expected_stdout
