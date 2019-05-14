import json
from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('book_backend')


def get_table_ref(name):
    return dataset_ref.table(name)


def create_inventory_table(table_ref=get_table_ref("book_inventory")):
    schema = [
        bigquery.SchemaField("title", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("subtitle", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("authors", "STRING", mode="REPEATED"),
        bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("categories", "STRING", mode="REPEATED"),
        bigquery.SchemaField("id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("maturity", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("preview_link", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("embeddable", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField(
            "industry_identifiers",
            "RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField("ISBN_13", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("ISBN_10", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("OTHER", "STRING", mode="NULLABLE")]),
        bigquery.SchemaField("snippet", "STRING", mode="NULLABLE")
    ]

    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)


def create_error_table(table_ref=get_table_ref("failed_books")):
    schema = [
        bigquery.SchemaField("filename", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("error", "STRING", mode="NULLABLE")
    ]

    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)


def load_book_from_ndjson(table_name):
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    if table_name == "book_inventory":
        path = 'temp/book_info.ndjson'
    elif table_name == "failed_books":
        path = 'temp/book_error.ndjson'

    with open(path, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            get_table_ref(table_name),
            location="US",
            job_config=job_config,
        )

    job.result()
