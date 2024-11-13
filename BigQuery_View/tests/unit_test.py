import unittest
from unittest.mock import patch

from google.cloud import bigquery

from your_module import query_view


class TestQueryView(unittest.TestCase):
    @patch("google.cloud.bigquery.Client")
    def test_query_view_success(self, mock_client):
        # Mock the query job result
        mock_query_job = mock_client.return_value.query.return_value
        mock_query_job.result.return_value = [
            {"Id": 1, "Name": "Vijay"},
            {"Id": 3, "Name": "John"},
        ]

        # Call the function
        result = query_view(None)

        # Assert the expected output
        self.assertEqual(result, "Query Executed Successfully...")
        self.assertEqual(mock_client.call_count, 1)
        self.assertEqual(mock_client.call_args[0], (("sre-project-poc",),))
        self.assertEqual(mock_client.return_value.query.call_count, 1)
        self.assertEqual(
            mock_client.return_value.query.call_args[0],
            (
                (
                    "SELECT * FROM `sre-project-poc.test_dataset.test_table_view`",
                    (),
                ),
            ),
        )

    @patch("google.cloud.bigquery.Client")
    def test_query_view_failure(self, mock_client):
        # Mock the query job exception
        mock_query_job = mock_client.return_value.query.return_value
        mock_query_job.result.side_effect = Exception("Query failed")

        # Call the function
        result = query_view(None)

        # Assert the expected output
        self.assertEqual(result, "Failed to query the view: Query failed")
        self.assertEqual(mock_client.call_count, 1)
        self.assertEqual(mock_client.call_args[0], (("sre-project-poc",),))
        self.assertEqual(mock_client.return_value.query.call_count, 1)
        self.assertEqual(
            mock_client.return_value.query.call_args[0],
            (
                (
                    "SELECT * FROM `sre-project-poc.test_dataset.test_table_view`",
                    (),
                ),
            ),
        )

    @patch("google.cloud.bigquery.Client")
    def test_query_view_ceo_output(self, mock_client):
        # Mock the query job result
        mock_query_job = mock_client.return_value.query.return_value
        mock_query_job.result.return_value = [
            {"Id": 1, "Name": "Vijay"},
            {"Id": 3, "Name": "John"},
        ]

        # Call the function
        query_view(None)

        # Assert the expected output
        self.assertIn("CEO: Vijay", self.maxDiff)
        self.assertIn("Normal Employee: John", self.maxDiff)

    @patch("google.cloud.bigquery.Client")
    def test_query_view_employee_output(self, mock_client):
        # Mock the query job result
        mock_query_job = mock_client.return_value.query.return_value
        mock_query_job.result.return_value = [
            {"Id": 3, "Name": "John"},
            {"Id": 4, "Name": "Jane"},
        ]

        # Call the function
        query_view(None)

        # Assert the expected output
        self.assertNotIn("CEO: John", self.maxDiff)
        self.assertIn("Normal Employee: John", self.maxDiff)
        self.assertIn("Normal Employee: Jane", self.maxDiff)
