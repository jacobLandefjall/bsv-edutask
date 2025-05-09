"""
Design and implement integration tests for the communication between the data access object DAO
(backend/src/util/dao.py) and the Mongo database focusing on the create method. 
"""

import pytest
import pymongo
from src.util.dao import DAO
from pymongo.errors import WriteError
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime

def test_validator():
    """
    Validator function to define the schema for the MongoDB collection.
    """
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "description", "startdate", "duedate"],
            "properties": {
                "title": {"bsonType": "string"},
                "description": {"bsonType": "string"},
                "startdate": {"bsonType": "date"},
                "duedate": {"bsonType": "date"}
            }
        }
    }


@pytest.fixture
# pytest fixture to create a temporary MongoDB collection for testing.
def dao_test_collection():
    """
    Setup a temporary MongoDB collection for testing and database.
    - Connects to a test-only database.
    - Creates a temporary collection with a schema validator.
    - Yields a DAO instance for isolated testing.
    - Cleans up afterward by dropping the collection.
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
        validator=test_validator()
    )
    dao = DAO(test_collection_name)

    yield dao # Provide the DAO instance to the test

    # Teardown: Drop the test collection and database
    test_db.drop_collection(test_collection_name)

def test_create_valid_document(dao_test_collection):
    """
    Testing the creation of a valid document in the collection.
    Given: A dictionary containing all required and correctly typed fields.
    Expectation: The DAO.create() method successfully inserts the document and returns it.
    """
    valid_data = {
        "title": "Test Document",
        "description": "A test document",
        "startdate": datetime(2025, 4, 22),
        "duedate": datetime(2025, 4, 25),
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
    Given: A document missing the 'description' field.
    Expectation: DAO.create() raises a WriteError due to validation failure.
    """
    invalid_data = {
        "title": "Valid Title", 
        "description": "Valid description", 
        "startdate": 12345,  # Invalid type (should be a string or date)
        "duedate": "2025-04-25T00:00:00", 
        "requires": [ObjectId()],
        "categories": ["work", "urgent"],
        "todos": [ObjectId()],
        "video": ObjectId()
    }

    with pytest.raises(WriteError):
        dao_test_collection.create(invalid_data)


def test_create_missing_required_field(dao_test_collection):
    """
    Testing the creation of a document with missing required fields.
    Given: A document with 'title', but missing other mandatory fields like 'description'.
    Expectation: WriteError is raised indicating schema validation failure.
    """
    invalid_data = {
        "title": 12345,  # Invalid type for title
        # Missing required field 'description'
        "startdate": "2025-04-22T00:00:00",
        "duedate": "2025-04-25T00:00:00"
    }

    with pytest.raises(WriteError):
        dao_test_collection.create(invalid_data)

def test_create_wrong_data_type(dao_test_collection):
    """
    Testing the creation of a document with wrong data types.
    Given: A document where 'duedate' is a string not in ISO date format.
    Expectation: WriteError is raised due to schema/type mismatch.
    """
    invalid_data = {
        "title": 12345,  # Invalid type for title
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

def test_create_with_high_value(dao_test_collection):
    """
    Testing the creation of a document with a high value input (e.g., above 120).
    Given: A document with a field that exceeds the normal range.
    Expectation: The system should handle the high value appropriately, either by rejecting it or processing it correctly.
    """
    high_value_data = {
        "title": "High Value Document",
        "description": "A document with high value",
        "startdate": datetime(2025, 4, 22),
        "duedate": datetime(2025, 4, 22),
        "requires": [ObjectId()],
        "categories": ["work", "urgent"],
        "todos": [ObjectId()],
        "video": ObjectId(),
        "value": 130  # Value exceeding 120
    }
    result = dao_test_collection.create(high_value_data)
    assert "_id" in result
    assert result["value"] == 130


def test_create_with_invalid_sensor_time(dao_test_collection):
    """
    Testing the creation of a document where the sensor time condition is invalid.
    Given: A document where sensor time is incorrectly set.
    Expectation: WriteError is raised due to invalid sensor time handling.
    """
    invalid_sensor_time_data = {
        "title": "Sensor Time Document",
        "description": "A document with an invalid sensor time",
        "startdate": datetime(2025, 4, 22),
        "duedate": datetime(2025, 4, 22),
        "requires": [ObjectId()],
        "categories": ["work", "urgent"],
        "todos": [ObjectId()],
        "video": ObjectId(),
        "sensor_time": "invalid"  # Invalid sensor time data
    }

    with pytest.raises(WriteError):
        dao_test_collection.create(invalid_sensor_time_data)


def test_create_missing_card_condition(dao_test_collection):
    """
    Testing the creation of a document where the card condition is missing.
    Given: A document where card condition data is absent.
    Expectation: WriteError should be raised as this is a required field.
    """
    missing_card_condition_data = {
        "title": "Card Condition Document",
        "description": "A document missing the card condition",
        "startdate": datetime(2025, 4, 22),
        "duedate": datetime(2025, 4, 22),
        "requires": [ObjectId()],
        "categories": ["work", "urgent"],
        "todos": [ObjectId()],
        "video": ObjectId(),
        # Missing card condition data}
    }

    with pytest.raises(WriteError):
        dao_test_collection.create(missing_card_condition_data)
