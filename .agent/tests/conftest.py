"""Shared fixtures: a fresh run state at the defaults (every row's fast method already run)."""

import pytest

from aerosim.core.state import State


@pytest.fixture
def state():
    return State()
