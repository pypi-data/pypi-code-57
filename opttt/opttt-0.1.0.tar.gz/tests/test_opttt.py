"""Tests for `opttt` package."""

import pathlib
import uuid

from pydantic import Field

from opttt import Opttt


def test_print():
    """Test that the print command is properly parsed."""

    class Options(Opttt):

        a: int
        b: int

        class Config:
            name: str = "The application."
            description: str = "The description."

    options = Options.from_args(["1", "2"])

    assert options.a == 1
    assert options.b == 2


def test_optional():
    """Test optional arguments work."""

    class DefaultOptions(Opttt):

        b: int
        a: int = Field(1, description="Help for A.")

        class Config:
            name: str = "The application."
            description: str = "The description."

    options = DefaultOptions.from_args(["2"])
    assert options.a == 1

    options = DefaultOptions.from_args(["2", "--a", "2"])
    assert options.a == 2


def test_complex_char():
    """Test a complex type."""

    class DefaultOptions(Opttt):

        b: pathlib.Path
        a: uuid.UUID

        class Config:
            name: str = "The application."
            description: str = "The description."

    options = DefaultOptions.from_args(["./", "0321fd6a-7374-4536-a5e3-df3673d3427b"])
    assert options.a == uuid.UUID("0321fd6a-7374-4536-a5e3-df3673d3427b")
    assert options.b == pathlib.Path("./")
