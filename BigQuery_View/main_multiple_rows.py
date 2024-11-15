from google.cloud import bigquery
import os
import json

def query_view(data):
    try:
        config_file = os.environ.get("FILE_JSON")
        with open(config_file, 'r') as file:
            config = json.load(file)
    
        project_id = config['settings']['project_id']
        dataset_id = config['settings']['dataset_id']
        view_id = config['settings']['view_id']
        client = bigquery.Client(project=project_id)

        # Qualify the view with its dataset and project.
        view_ref = f"{project_id}.{dataset_id}.{view_id}"

        # Construct a full SQL query.
        query = f"SELECT * FROM `{view_ref}`"

    except Exception as e:
        print(f"Config file not present: {e}")
        return "Not Done"

    try:
        # Execute the query. Wait for the job to finish
        query_job = client.query(query)
        
        # Fetch the results and process them
        results = query_job.result()  # Waits for the job to complete
        
        for row in results:
            Id = int(row['Id'])
            name = row['Name']
            if Id <= 2:
                print(f"CEO: {name}")
            else:
                print(f"Normal Employee: {name}")
        print("Query Executed Successfully...")
        return "Done"
    except Exception as e:
        print(f"Failed to query the view: {e}")
        return "Not Done"
