"""User domain entity."""

from __future__ import annotations

import re
from dataclasses import dataclass

from entity.exceptions import InvalidUserError

MIN_DISPLAY_NAME_LENGTH = 2
MAX_DISPLAY_NAME_LENGTH = 50
MAX_USER_ID_LENGTH = 64
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True, slots=True)
class User:
    """Represents an application user in the MagicSquare domain.

    Immutable value object holding identity and contact data.
    All invariants are enforced at construction time.

    Attributes:
        user_id: Unique identifier (non-empty, max 64 characters).
        display_name: Human-readable name shown in UI and logs.
        email: Optional email address; must match basic format if set.
    """

    user_id: str
    display_name: str
    email: str | None = None

    def __post_init__(self) -> None:
        """Validate fields after dataclass initialization."""
        self._validate_user_id(self.user_id)
        self._validate_display_name(self.display_name)
        if self.email is not None:
            self._validate_email(self.email)

    @classmethod
    def create(
        cls,
        user_id: str,
        display_name: str,
        email: str | None = None,
    ) -> User:
        """Create a User after validating all fields.

        Args:
            user_id: Unique identifier for the user.
            display_name: Name shown in the application.
            email: Optional contact email.

        Returns:
            A validated User instance.

        Raises:
            InvalidUserError: If any field fails validation.
        """
        normalized_id = user_id.strip()
        normalized_name = display_name.strip()
        normalized_email: str | None = None
        if email is not None:
            normalized_email = email.strip()
            if not normalized_email:
                raise InvalidUserError("email must not be empty or whitespace only")
        return cls(
            user_id=normalized_id,
            display_name=normalized_name,
            email=normalized_email,
        )

    def with_display_name(self, display_name: str) -> User:
        """Return a copy with an updated display name.

        Args:
            display_name: New display name.

        Returns:
            New User instance with updated display_name.

        Raises:
            InvalidUserError: If display_name fails validation.
        """
        return User.create(
            user_id=self.user_id,
            display_name=display_name,
            email=self.email,
        )

    def with_email(self, email: str | None) -> User:
        """Return a copy with an updated or cleared email.

        Args:
            email: New email, or None to clear.

        Returns:
            New User instance with updated email.

        Raises:
            InvalidUserError: If email fails validation.
        """
        return User.create(
            user_id=self.user_id,
            display_name=self.display_name,
            email=email,
        )

    @staticmethod
    def _validate_user_id(user_id: str) -> None:
        if not user_id:
            raise InvalidUserError("user_id must not be empty")
        if len(user_id) > MAX_USER_ID_LENGTH:
            raise InvalidUserError(
                f"user_id must not exceed {MAX_USER_ID_LENGTH} characters"
            )

    @staticmethod
    def _validate_display_name(display_name: str) -> None:
        if len(display_name) < MIN_DISPLAY_NAME_LENGTH:
            raise InvalidUserError(
                f"display_name must be at least {MIN_DISPLAY_NAME_LENGTH} characters"
            )
        if len(display_name) > MAX_DISPLAY_NAME_LENGTH:
            raise InvalidUserError(
                f"display_name must not exceed {MAX_DISPLAY_NAME_LENGTH} characters"
            )

    @staticmethod
    def _validate_email(email: str) -> None:
        if not _EMAIL_PATTERN.match(email):
            raise InvalidUserError("email format is invalid")
