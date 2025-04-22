"""
Design and implement integration tests for the communication between the data access object DAO
(backend/src/util/dao.py) and the Mongo database focusing on the create method. 
"""

import pytest
import pymongo
from src.util.dao import DAO
from src.util.validators import getValidator
from pymongo.errors import WriteError
from pymongo import MongoClient
from bson import ObjectId
import os

@pytest.fixture
# pytest fixture to create a temporary MongoDB collection for testing.
def dao_test_collection():
    """
    Setup a temporary MongoDB collection for testing and database.
    """
    test_db_name = "test_db"
    test_collection_name = "test_collection"
    mongo_url = "mongodb://root:root@mongodb:27017"

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_url)

    # Create a test database and collection
    test_db = client[test_db_name]

    # Drop if the collection already exists
    if test_collection_name in test_db.list_collection_names():
        test_db.drop_collection(test_collection_name)

    # Use validator for the collection
    test_db.create_collection(
        test_collection_name,
        validator=getValidator(test_collection_name)
    )
    dao = DAO(test_collection_name)

    yield dao # Provide the DAO instance to the test

    # Teardown: Drop the test collection and database
    test_db.drop_collection(test_collection_name)

def test_create_valid_document(dao_test_collection):
    """
    Testing the creation of a valid document in the collection.
    """
    valid_data = {
        "title": "Test Document",
        "description": "A test document",
        "startdate": "2025-04-22T00:00:00",
        "duedate": "2025-04-25T00:00:00",
        "requires": [ObjectId()],
        "categories": ["work", "urgent"],
        "todos": [ObjectId()],
        "video": ObjectId()
    }

    result = dao_test_collection.create(valid_data)
    assert "_id" in result
    assert result["title"] == "Test Document"
    assert result["description"] == "A test document"

def test_create_invalid_document(dao_test_collection):
    """
    Testing the creation of an invalid document in the collection.
    """
    invalid_data = {
        "title": "Test Document",
        # Missing required field 'description'
        "startdate": "2025-04-22T00:00:00",
        "duedate": "2025-04-25T00:00:00"
    }

    with pytest.raises(WriteError):
        dao_test_collection.create(invalid_data)


def test_create_missing_required_field(dao_test_collection):
    """
    Testing the creation of a document with missing required fields.
    """
    invalid_data = {
        "title": "Test Document",
        # Missing required field 'description'
        "startdate": "2025-04-22T00:00:00",
        "duedate": "2025-04-25T00:00:00"
    }

    with pytest.raises(WriteError):
        dao_test_collection.create(invalid_data)

def test_create_wrong_data_type(dao_test_collection):
    """
    Testing the creation of a document with wrong data types.
    """
    invalid_data = {
        "title": "Test Document",
        "description": "A test task description",
        "startdate": "2025-04-22T00:00:00",  # Correct data type
        "duedate": "Invalid date",  # Wrong data type (should be a date)
        "requires": [ObjectId()],
        "categories": ["work", "urgent"],
        "todos": [ObjectId()],
        "video": ObjectId()
    }

    with pytest.raises(WriteError):
        dao_test_collection.create(invalid_data)
