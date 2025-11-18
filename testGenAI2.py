from google.cloud import bigquery
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("PROJECT_ID"))


def run_bq_query(sql):
    # Path to your service account key file
    key_path = 'c:\\rock-sublime-446111-j0-749165cceca6.json'
    credentials = Credentials.from_service_account_file(key_path,
                                                        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    if credentials.expired:
        credentials.refresh(Request())

    # Create BQ client
    bq_client = bigquery.Client(project=os.getenv("PROJECT_ID"), credentials=credentials)

    # Try dry run before executing query to catch any errors
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    bq_client.query(sql, job_config=job_config)

    # If dry run succeeds without errors, proceed to run query
    job_config = bigquery.QueryJobConfig()
    client_result = bq_client.query(sql, job_config=job_config)
    job_id = client_result.job_id

    # Wait for query/job to finish running. then get & return data frame
    df = client_result.result().to_arrow().to_pandas()
    print(f"Finished job_id: {job_id}")
    return df


language_list = ["python", "html"]
so_df = pd.DataFrame()

for language in language_list:
    print(f"generating {language} dataframe")

    query = f"""
    SELECT
        CONCAT(q.title, q.body) as input_text,
        a.body AS output_text
    FROM
        `bigquery-public-data.stackoverflow.posts_questions` q
    JOIN
        `bigquery-public-data.stackoverflow.posts_answers` a
    ON
        q.accepted_answer_id = a.id
    WHERE 
        q.accepted_answer_id IS NOT NULL AND 
        REGEXP_CONTAINS(q.tags, "{language}") AND
        a.creation_date >= "2020-01-01"
    LIMIT 
        500
    """

    language_df = run_bq_query(query)
    language_df["category"] = language
    so_df = pd.concat([so_df, language_df], ignore_index=True)
    print(so_df)
