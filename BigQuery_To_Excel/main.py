import os
import pandas as pd
from google.cloud import bigquery

def query_and_email(request):
    # Set up BigQuery Client
    client = bigquery.Client()
    query = """
        SELECT * FROM `sre-project-poc.test_dataset.test_table` 
        LIMIT 1000
    """
    df = client.query(query).to_dataframe()

    # Save DataFrame to an Excel file
    excel_file = "/tmp/query_results.xlsx"
    df.to_excel(excel_file, index=False)

    df_read_back = pd.read_excel('/tmp/query_results.xlsx')
    print(df_read_back)
    return "Writing Data in to Excel is Complete"
