from google.cloud import bigquery

def run_query_from_file(data):
    file_path = './sql_query.sql'
    project_id = "sre-project-poc"
    # Construct a BigQuery client object.
    client = bigquery.Client(project=project_id)

    # Read the query from the file
    with open(file_path, 'r') as file:
        query = file.read()

    # Run the query and wait for the job to complete
    query_job = client.query(query)

    try:
        # Fetch the result
        results = query_job.result()  # Waits for the query to finish

        for row in results:
            print(row['Actual_Count'])  # Example of accessing data; could map to a different function or processing
            count = row['Actual_Count']
        if count == "2":
            print(f"Data Quality Test Results is: {True}")
        else:
            print(f"Data Quality Test Results is: {False}")
        return "Query Execution Completed..."
    except Exception as e:
        print(f"An error occurred for Query: {e}")
