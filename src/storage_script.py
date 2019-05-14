from google.cloud import storage


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    return [blob.name for blob in blobs]


def move_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
    """Copies a blob from one bucket to another with a new name."""
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)

    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)
    
    source_blob.delete()

    print('Blob {} in bucket {} copied to blob {} in bucket {}.'.format(
        source_blob.name, source_bucket.name, new_blob.name,
        destination_bucket.name))
    print('Blob {} deleted.'.format(source_blob))


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))