import json
from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('book_backend')
table_ref = dataset_ref.table("book_inventory")

def create_inventory_table(table_ref=table_ref):
    schema = [
        bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("title", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("subtitle", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("authors", "STRING", mode="REPEATED"),
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
        bigquery.SchemaField("snippet", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("categories", "STRING", mode="REPEATED")
    ]

    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)


def load_book_from_ndjson():
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    with open('temp/book_info.ndjson', "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location="US",
            job_config=job_config,
        )

    job.result()
