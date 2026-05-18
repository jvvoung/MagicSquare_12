"""Tests for entity.user.User."""

from __future__ import annotations

import pytest

from entity.exceptions import InvalidUserError
from entity.user import (
    MAX_DISPLAY_NAME_LENGTH,
    MAX_USER_ID_LENGTH,
    MIN_DISPLAY_NAME_LENGTH,
    User,
)


class TestUserCreate:
    """Tests for User.create and construction."""

    def test_create_valid_user_with_email(
        self,
        valid_user_id: str,
        valid_display_name: str,
        valid_email: str,
    ) -> None:
        """User.create succeeds with valid id, name, and email."""
        # Arrange & Act
        user = User.create(
            user_id=valid_user_id,
            display_name=valid_display_name,
            email=valid_email,
        )

        # Assert
        assert user.user_id == valid_user_id
        assert user.display_name == valid_display_name
        assert user.email == valid_email

    def test_create_valid_user_without_email(
        self,
        valid_user_id: str,
        valid_display_name: str,
    ) -> None:
        """User.create succeeds when email is omitted."""
        # Arrange & Act
        user = User.create(
            user_id=valid_user_id,
            display_name=valid_display_name,
        )

        # Assert
        assert user.email is None

    def test_empty_user_id_raises(
        self,
        valid_display_name: str,
    ) -> None:
        """Empty user_id raises InvalidUserError."""
        # Arrange & Act & Assert
        with pytest.raises(InvalidUserError, match="user_id"):
            User.create(user_id="   ", display_name=valid_display_name)

    def test_user_id_too_long_raises(
        self,
        valid_display_name: str,
    ) -> None:
        """user_id longer than MAX_USER_ID_LENGTH raises InvalidUserError."""
        # Arrange
        long_id = "x" * (MAX_USER_ID_LENGTH + 1)

        # Act & Assert
        with pytest.raises(InvalidUserError, match="user_id"):
            User.create(user_id=long_id, display_name=valid_display_name)

    def test_display_name_too_short_raises(
        self,
        valid_user_id: str,
    ) -> None:
        """display_name shorter than minimum raises InvalidUserError."""
        # Arrange
        short_name = "a" * (MIN_DISPLAY_NAME_LENGTH - 1)

        # Act & Assert
        with pytest.raises(InvalidUserError, match="display_name"):
            User.create(user_id=valid_user_id, display_name=short_name)

    def test_display_name_too_long_raises(
        self,
        valid_user_id: str,
    ) -> None:
        """display_name longer than maximum raises InvalidUserError."""
        # Arrange
        long_name = "a" * (MAX_DISPLAY_NAME_LENGTH + 1)

        # Act & Assert
        with pytest.raises(InvalidUserError, match="display_name"):
            User.create(user_id=valid_user_id, display_name=long_name)

    def test_invalid_email_raises(
        self,
        valid_user_id: str,
        valid_display_name: str,
    ) -> None:
        """Malformed email raises InvalidUserError."""
        # Arrange & Act & Assert
        with pytest.raises(InvalidUserError, match="email"):
            User.create(
                user_id=valid_user_id,
                display_name=valid_display_name,
                email="not-an-email",
            )

    def test_empty_email_string_raises(
        self,
        valid_user_id: str,
        valid_display_name: str,
    ) -> None:
        """Whitespace-only email raises InvalidUserError."""
        # Arrange & Act & Assert
        with pytest.raises(InvalidUserError, match="email"):
            User.create(
                user_id=valid_user_id,
                display_name=valid_display_name,
                email="   ",
            )


class TestUserImmutability:
    """Tests for immutable update helpers."""

    def test_with_display_name_returns_new_instance(
        self,
        sample_user: User,
    ) -> None:
        """with_display_name returns a new User without mutating original."""
        # Arrange
        new_name = "Square Master"

        # Act
        updated = sample_user.with_display_name(new_name)

        # Assert
        assert updated.display_name == new_name
        assert updated.user_id == sample_user.user_id
        assert updated.email == sample_user.email
        assert sample_user.display_name != new_name

    def test_with_email_returns_new_instance(
        self,
        sample_user: User,
    ) -> None:
        """with_email returns a new User with updated email."""
        # Arrange
        new_email = "master@example.com"

        # Act
        updated = sample_user.with_email(new_email)

        # Assert
        assert updated.email == new_email
        assert sample_user.email != new_email

    def test_with_email_none_clears_email(
        self,
        sample_user: User,
    ) -> None:
        """with_email(None) clears the email field."""
        # Arrange & Act
        updated = sample_user.with_email(None)

        # Assert
        assert updated.email is None

    def test_frozen_user_is_hashable(
        self,
        sample_user: User,
    ) -> None:
        """Frozen User instances can be used in sets and as dict keys."""
        # Arrange & Act
        users = {sample_user}

        # Assert
        assert sample_user in users
