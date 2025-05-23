"""
Assignment 2:
An implementation of test cases using Pytest
Lich23 and jalf23
Tests are Designed According to Ground Truth (Docstring)
Designed tests around the expected behavior outlined in the docstring.
"""

import pytest
from src.controllers.usercontroller import UserController
from unittest.mock import MagicMock

@pytest.fixture # Fixture: Think of preparing specific records in the database.
def mock_dao():
    return MagicMock()

@pytest.fixture
def controller(mock_dao):
    return UserController(mock_dao)

def test_single_user_exist(controller, mock_dao):
    """
    Test function to check if the user exists.
    """
    mock_user = {"email": "tryuser@student.bth.se"}
    mock_dao.find.return_value = [mock_user] # mock to return a list with one user.

    result = controller.get_user_by_email("tryuser@student.bth.se")

    assert result == mock_user # Check if the result is the same as the mock user.

def test_multiple_users_exist_returns_first(controller, mock_dao):
    """
    Test function to check if the first user is returned when multiple users exist.
    """
    # Mocking the behavior of the DAO to return multiple users.
    mock_users = [{"email": "tryuser@student.bth.se"}, {"email": "tryuser@student.bth.se"}]
    mock_dao.find.return_value = mock_users

    result = controller.get_user_by_email("tryuser@student.bth.se")

    assert result == mock_users[0]

def test_multiple_users_exist_logs_warning(controller, mock_dao, capsys):
    """
    Test function to check if a warning is logged when multiple users exist.
    """
    # Mocking the behavior of the DAO to return multiple users.
    mock_users = [{"email": "tryuser@student.bth.se"}, {"email": "tryuser@student.bth.se"}]
    mock_dao.find.return_value = mock_users

    controller.get_user_by_email("tryuser@student.bth.se")
    captured = capsys.readouterr()

    assert "Error: more than one user found with mail tryuser@student.bth.se" in captured.out

def test_user_not_found(controller, mock_dao):
    """
    Test function to check if the user is not found.
    """
    mock_dao.find.return_value = [] # mock to return an empty list.

    with pytest.raises(IndexError): # IndexError due to users being empty.
        controller.get_user_by_email("missing@student.bth.se")

def test_invalid_email(controller):
    """
    Test function to check if the email is invalid.
    """
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalidemail")

def test_empty_email(controller):
    """
    Test function to check if an empty email results in an error.
    """
    with pytest.raises(ValueError):
        controller.get_user_by_email("")

def test_minimal_valid_email(controller, mock_dao):
    """
    Test function to check if the email is valid on the minimal level.
    """
    mock_user = {"email": "a@b.c"}
    mock_dao.find.return_value = [mock_user] # mock to return a list with one user.

    result = controller.get_user_by_email("a@b.c")

    assert result == mock_user # Check if the result is the same as the mock user.

def test_database_exceptions(controller, mock_dao):
    """
    Test function to check if the database exceptions are handled.
    """
    mock_dao.find.side_effect = Exception("Database error") # mock to raise an exception.

    with pytest.raises(Exception):
        controller.get_user_by_email("tryuser@student.bth.se")
