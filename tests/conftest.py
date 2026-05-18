"""Shared pytest fixtures for MagicSquare tests."""

from __future__ import annotations

import pytest

from entity.user import User


@pytest.fixture
def valid_user_id() -> str:
    """Return a valid user identifier."""
    return "user-001"


@pytest.fixture
def valid_display_name() -> str:
    """Return a valid display name."""
    return "Magic Fan"


@pytest.fixture
def valid_email() -> str:
    """Return a valid email address."""
    return "fan@example.com"


@pytest.fixture
def sample_user(
    valid_user_id: str,
    valid_display_name: str,
    valid_email: str,
) -> User:
    """Return a fully valid User for reuse in tests."""
    return User.create(
        user_id=valid_user_id,
        display_name=valid_display_name,
        email=valid_email,
    )
