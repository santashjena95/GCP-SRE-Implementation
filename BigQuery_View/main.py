from google.cloud import bigquery

def query_view(data):
    project_id = 'sre-project-poc'  # Replace with your project ID
    dataset_id = 'test_dataset'  # Replace with your dataset ID
    view_id = 'test_table_view'  # Replace with your view ID
    # Build a BigQuery client object.
    client = bigquery.Client(project=project_id)

    # Qualify the view with its dataset and project.
    view_ref = f"{project_id}.{dataset_id}.{view_id}"

    # Construct a full SQL query.
    query = f"SELECT * FROM `{view_ref}`"

    # Execute the query. Wait for the job to finish
    query_job = client.query(query)

    try:
        # Fetch the results and process them
        results = query_job.result()  # Waits for the job to complete
        for row in results:
            print(row['f0_'])  # Do something meaningful with the rows
            count = row['f0_']
        if count == "2":
            print(f"Data Quality Test Results is: {True}")
        else:
            print(f"Data Quality Test Results is: {False}")
        return "Query Executed Successfully..."
    except Exception as e:
        print(f"Failed to query the view: {e}")
