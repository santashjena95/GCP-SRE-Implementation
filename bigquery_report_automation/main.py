from google.cloud import logging
from google.cloud import bigquery
from google.cloud import storage
import pandas as pd
from datetime import date, timedelta

def create_and_upload_csv(sum_interaction_ids, sum_trs_interactions_success, sum_difference, percent_failed, bucket_name, destination_blob_name, project_id, order_date, today, google_alternate_error_count, zero_sec_call_error_count, end_offset_error_count):

    data = {
        "Order Date": [order_date],
        "Process Date": [today],
        "PR2 Interactions": [sum_interaction_ids],
        "Transcripts Success": [sum_trs_interactions_success],
        "Difference": [sum_difference],
        "% failed": [percent_failed],
        "alternatives attribute missing from google generated transcript (Reprocessing not required)": [google_alternate_error_count],
        "Error: ffmpeg exited with code 1 (Zero Sec Call) (Reprocessing not required)": [zero_sec_call_error_count],
        "Something went wrong in construct_transcript_json: 'endOffset'": [end_offset_error_count]
    }
    df = pd.DataFrame(data)

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(df.to_csv(index=False), 'text/csv')
    print(f"File uploaded to {destination_blob_name}.")

def list_logs(project_id, log_name, today):
    
    client = logging.Client(project=project_id)
    extract_time = today+"T00:00:00.000Z"
    time_filter = f'timestamp>="{extract_time}"'
    filter_str = f'resource.type="cloud_function" AND textPayload =~ "Total records retrieved from PR2:*" AND logName="projects/{project_id}/logs/{log_name}" AND {time_filter}'

    for entry in client.list_entries(filter_=filter_str):
        timestamp = entry.timestamp.isoformat()
        number_str = entry.payload.split(": ")[1]
        number = int(number_str)
        return number

def execute_query(project_id, query):
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    results = query_job.result()
    df = results.to_dataframe()
    return df

def read_query_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def execution_start(request):
    project_id = 'turnkey-cove-443706-t1'
    log_name = 'cloudfunctions.googleapis.com%2Fcloud-functions'
    today = str(date.today())
    bucket_name = "sensor_data_input_demo"
    destination_blob_name = "sensor_data_"+today+".csv"
    log_num = list_logs(project_id, log_name, today)
    if log_num:
        query_file_path = 'execute.sql'
        sql_query = read_query_from_file(query_file_path)
        df = execute_query(project_id, sql_query)
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
        order_date = str(date.today() - timedelta(days=1))

        request_guid_list = df['request_guid'].astype(str).tolist()
        formatted_guids = '"' + '","'.join(request_guid_list) + '"'
        end_offset_error_query = """
        SELECT DISTINCT interaction_id, message 
        FROM `voice_surv_stt.voice_surv_transcript_audit` 
        WHERE insertion_date BETWEEN DATETIME("{}") AND DATETIME_ADD(DATETIME("{}"), INTERVAL 1 DAY) 
        AND request_guid IN ({})
        AND status="Failed"
        AND message LIKE "%construct_transcript_json: 'endOffset'"
        """
        formatted_end_offset_error_query = end_offset_error_query.format(today, today, formatted_guids)
        end_offset_error_count = execute_bigquery_count(formatted_end_offset_error_query, project_id)
        google_alternate_error_query = """
        SELECT DISTINCT interaction_id, message 
        FROM `voice_surv_stt.voice_surv_transcript_audit` 
        WHERE insertion_date BETWEEN DATETIME("{}") AND DATETIME_ADD(DATETIME("{}"), INTERVAL 1 DAY) 
        AND request_guid IN ({})
        AND status="Failed"
        AND message LIKE "%generated transcript."
        """
        formatted_google_alternate_error_query = google_alternate_error_query.format(today, today, formatted_guids)
        google_alternate_error_count = execute_bigquery_count(formatted_google_alternate_error_query, project_id)
        zero_sec_call_error_query = """
        SELECT DISTINCT interaction_id, message 
        FROM `voice_surv_stt.voice_surv_transcript_audit` 
        WHERE insertion_date BETWEEN DATETIME("{}") AND DATETIME_ADD(DATETIME("{}"), INTERVAL 1 DAY) 
        AND request_guid IN ({})
        AND status="Failed"
        AND message LIKE "%transcript not exist"
        """
        formatted_zero_sec_call_error_query = zero_sec_call_error_query.format(today, today, formatted_guids)
        zero_sec_call_error_count = execute_bigquery_count(formatted_zero_sec_call_error_query, project_id)
        create_and_upload_csv(sum_interaction_ids, sum_trs_interactions_success, sum_difference, percent_failed, bucket_name, destination_blob_name, project_id, order_date, today, google_alternate_error_count, zero_sec_call_error_count, end_offset_error_count)
    else:
        print('No "Total records retrieved from PR2:" logs present for today')

execution_start(request)
