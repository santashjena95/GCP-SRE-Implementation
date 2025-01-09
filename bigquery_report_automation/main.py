from google.cloud import logging
from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta, timezone

def list_logs(project_id, log_name, days_ago):
    # Create a logging client
    client = logging.Client(project=project_id)
    
    # Format the time range (last 24 hours)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days_ago)
    
    # Convert times to RFC3339 datetime string format without microseconds
    end_time = end_time.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    start_time = start_time.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    
    # Create a filter string for the time range
    time_filter = f'timestamp>="{start_time}" AND timestamp<="{end_time}"'

    # Combine log name with time filter
    filter_str = f'resource.type="cloud_function" AND textPayload =~ "Total records retrieved from PR2:*" AND logName="projects/{project_id}/logs/{log_name}" AND {time_filter}'

    # List all entries in the log
    for entry in client.list_entries(filter_=filter_str):  # API call(s)
        timestamp = entry.timestamp.isoformat()

        # Split the string by ': ' and get the second part
        number_str = entry.payload.split(": ")[1]

        # Convert the extracted string to an integer
        number = int(number_str)

        return number

def execute_query(project_id, query):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # Run the query and save the results to a pandas DataFrame
    query_job = client.query(query)  # Make an API request

    # Wait for the query to complete
    results = query_job.result()
    
    # Convert results to a pandas DataFrame
    df = results.to_dataframe()

    return df


if __name__ == '__main__':
    project_id = 'turnkey-cove-443706-t1'
    log_name = 'cloudfunctions.googleapis.com%2Fcloud-functions'  # e.g., "stderr", "syslog" or names of custom logs
    days_ago = 1   # Set to 1 for logs of the last 24 hours
    log_num = list_logs(project_id, log_name, days_ago)
    query = """
        SELECT *
        FROM `dataproc_gcs_to_bq.sample_python_table`
    """
    
    # Execute the query and get the result as pandas DataFrame
    df = execute_query(project_id, query)
    df['interaction_ids'] = pd.to_numeric(df['interaction_ids'])
    sum_interaction_ids = int(df['interaction_ids'].sum())
    if (log_num == sum_interaction_ids):
        print("All records processed successfully")
    else:
        print("Not All records processed successfully")
    df['trs_interactions_success'] = pd.to_numeric(df['trs_interactions_success'])
    sum_trs_interactions_success = df['trs_interactions_success'].sum()
    df['Difference'] = pd.to_numeric(df['Difference'])
    sum_difference = int(df['Difference'].sum())
    
    percent_failed = (sum_difference/sum_interaction_ids)*100
    print(percent_failed)
