# book_cover_reader

### This is an internal tool for the Tu Libro a Ciegas project, for managing the stock of available books using the Google Cloud Platform and Books API.

- Manages book photos within Google Storage
- Extract text from book's cover photos using Google Vision
- Searches for the desired book using the Google Books API
- Logs the info into Bigquery

#### The following variables should be defined within something like a .env file:
- GOOGLE_APPLICATION_CREDENTIALS: google cloud auth credentials
- bkt_todo: name of the google storage bucket with the unprocessed pictures
- bkt_done: name of the google storage bucket to move the successfully processed pictures to
- bkt_failed: name of the google storage bucket to move the failed pictures to
- dataset_name: name of the BigQuery dataset
- book_table: name of the table to log successfully processed books
- error_table: name of the table to log errors of failed pictures
