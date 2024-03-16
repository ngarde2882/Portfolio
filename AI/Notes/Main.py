import firebase_admin
from firebase_admin import credentials
import keys

firebase_admin.initialize_app(keys.firebase_cred, {'storageBucket': keys.firebase_url})

print('Hello World!')

file_path = "sample_image_file.jpg"
bucket = storage.bucket() # storage bucket
blob = bucket.blob(file_path)
blob.upload_from_filename(file_path)

file_path = "text_docs/sample_text_file.txt"
bucket = storage.bucket() # storage bucket
blob = bucket.blob(file_path)
blob.upload_from_filename(file_path)

from google.cloud import storage
from google.oauth2 import service_account
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    credentials = service_account.Credentials.from_service_account_file("path/to/your/credentials.json")
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
upload_blob(firebase_admin.storage.bucket().name, 'sample_image_file.jpg', 'images/beatiful_picture.jpg')