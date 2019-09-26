import os
import sys
import json
from google.cloud import bigquery

project_id = os.environ.get('gcloud_project')
dataset_name = os.environ.get('dataset_name')
book_table = os.environ.get('book_table')

client = bigquery.Client()
dataset_ref = client.dataset(dataset_name)


def get_table_ref(name):
    return dataset_ref.table(name)


def create_inventory_table(table_ref=get_table_ref(book_table)):
    schema = [
        bigquery.SchemaField("sequential_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("manual_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("title", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("subtitle", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("authors", "STRING", mode="REPEATED"),
        bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("categories", "STRING", mode="REPEATED"),
        bigquery.SchemaField("cover", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("back_cover", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("status", "INTEGER", mode="REQUIRED"),
    ]

    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)


def load_book_from_ndjson(table_name):
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    if table_name == book_table:
        if hasattr(sys, 'ps1'):
            path = '../temp/book_info.ndjson'
        else:
            path = 'temp/book_info.ndjson'

    with open(path, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            get_table_ref(table_name),
            location="US",
            job_config=job_config,
        )

    job.result()

def max_seq_id(project_id=project_id, dataset_name=dataset_name, table_name=book_table):
    QUERY = (
        'SELECT MAX(sequential_id) as rs FROM `' + project_id + '.' + dataset_name + '.' + table_name + '`')
    query_job = client.query(QUERY)

    return [row[0] for row in query_job][0]
