import pytest

from src.middle.users import valid_email


class TestUsersEmail:
    def test_valid_email(self):
        assert valid_email("asdf@example.com")
        assert valid_email("asdf.asdf@example.com")
        assert not valid_email("@example.com")
        assert not valid_email("example.com")
        assert not valid_email("asdf@example")


