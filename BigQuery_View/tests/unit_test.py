import pytest
from unittest.mock import Mock, patch, mock_open
import json
from src.main.main import query_view  # Replace 'your_module' with the actual module name

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

def test_query_view_success(mock_env, mock_bigquery_client, mock_open_file, capsys):
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
    assert result == "Done"
    mock_bigquery_client.assert_called_once_with(project='test-project')
    mock_bigquery_client.return_value.query.assert_called_once_with(
        "SELECT * FROM `test-project.test-dataset.test-view`"
    )
    mock_query_job.result.assert_called_once()

    captured = capsys.readouterr()
    assert "CEO: John Doe" in captured.out
    assert "CEO: Jane Smith" in captured.out
    assert "Normal Employee: Bob Johnson" in captured.out
    assert "Query Executed Successfully..." in captured.out

def test_query_view_config_file_error(mock_env, capsys):
    # Arrange
    with patch('builtins.open', side_effect=FileNotFoundError("Config file not found")):
        # Act
        result = query_view({})

    # Assert
    assert result == "Not Done"
    captured = capsys.readouterr()
    assert "Config file not present: Config file not found" in captured.out

def test_query_view_query_failure(mock_env, mock_bigquery_client, mock_open_file, capsys):
    # Arrange
    mock_query_job = Mock()
    mock_query_job.result.side_effect = Exception("Query failed")
    mock_bigquery_client.return_value.query.return_value = mock_query_job

    with patch('builtins.open', mock_open_file):
        # Act
        result = query_view({})

    # Assert
    assert result == "Not Done"
    mock_bigquery_client.assert_called_once_with(project='test-project')
    mock_bigquery_client.return_value.query.assert_called_once_with(
        "SELECT * FROM `test-project.test-dataset.test-view`"
    )
    mock_query_job.result.assert_called_once()

    captured = capsys.readouterr()
    assert "Failed to query the view: Query failed" in captured.out

def test_query_view_empty_results(mock_env, mock_bigquery_client, mock_open_file, capsys):
    # Arrange
    mock_query_job = Mock()
    mock_results = []
    mock_query_job.result.return_value = mock_results
    mock_bigquery_client.return_value.query.return_value = mock_query_job

    with patch('builtins.open', mock_open_file):
        # Act
        result = query_view({})

    # Assert
    assert result == "Done"
    mock_bigquery_client.assert_called_once_with(project='test-project')
    mock_bigquery_client.return_value.query.assert_called_once_with(
        "SELECT * FROM `test-project.test-dataset.test-view`"
    )
    mock_query_job.result.assert_called_once()

    captured = capsys.readouterr()
    assert "Query Executed Successfully..." in captured.out
    assert "CEO:" not in captured.out
    assert "Normal Employee:" not in captured.out
