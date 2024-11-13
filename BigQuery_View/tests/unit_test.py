import pytest
from unittest.mock import Mock, patch, mock_open
import json
from src.main.main import query_view

@pytest.fixture
def mock_config():
    return {
        "settings": {
            "project_id": "test-project",
            "dataset_id": "test-dataset",
            "view_id": "test-view"
        }
    }

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("FILE_JSON", "mock_config.json")

@pytest.fixture
def mock_bigquery_client():
    with patch('src.main.main.bigquery.Client') as mock_client:
        yield mock_client

@pytest.fixture
def mock_open_file(mock_config):
    return mock_open(read_data=json.dumps(mock_config))

def test_query_view_success(mock_env, mock_bigquery_client, mock_open_file):
    # Arrange
    mock_query_job = Mock()
    mock_results = [
        {'Id': '1', 'Name': 'John Doe'},
        {'Id': '2', 'Name': 'Jane Smith'},
        {'Id': '3', 'Name': 'Bob Johnson'}
    ]
    mock_query_job.result.return_value = mock_results
    mock_bigquery_client.return_value.query.return_value = mock_query_job

    with patch('builtins.open', mock_open_file):
        # Act
        result = query_view({})

    # Assert
    assert result == "Query Executed Successfully..."
    mock_bigquery_client.assert_called_once_with(project='test-project')
    mock_bigquery_client.return_value.query.assert_called_once_with(
        "SELECT * FROM `test-project.test-dataset.test-view`"
    )
    mock_query_job.result.assert_called_once()

def test_query_view_failure(mock_env, mock_bigquery_client, mock_open_file, capsys):
    # Arrange
    mock_query_job = Mock()
    mock_query_job.result.side_effect = Exception("Query failed")
    mock_bigquery_client.return_value.query.return_value = mock_query_job

    with patch('builtins.open', mock_open_file):
        # Act
        result = query_view({})

    # Assert
    assert result == None  # The function doesn't return anything when an exception occurs
    mock_bigquery_client.assert_called_once_with(project='test-project')
    mock_bigquery_client.return_value.query.assert_called_once_with(
        "SELECT * FROM `test-project.test-dataset.test-view`"
    )
    mock_query_job.result.assert_called_once()

    # Check that the error message was printed
    captured = capsys.readouterr()
    assert "Failed to query the view: Query failed" in captured.out

def test_query_view_print_output(mock_env, mock_bigquery_client, mock_open_file, capsys):
    # Arrange
    mock_query_job = Mock()
    mock_results = [
        {'Id': '1', 'Name': 'John Doe'},
        {'Id': '2', 'Name': 'Jane Smith'},
        {'Id': '3', 'Name': 'Bob Johnson'}
    ]
    mock_query_job.result.return_value = mock_results
    mock_bigquery_client.return_value.query.return_value = mock_query_job

    with patch('builtins.open', mock_open_file):
        # Act
        query_view({})

    # Assert
    captured = capsys.readouterr()
    assert "CEO: John Doe" in captured.out
    assert "CEO: Jane Smith" in captured.out
    assert "Normal Employee: Bob Johnson" in captured.out
