from datetime import datetime
from uuid import uuid4

from google.cloud import storage

from .settings import settings


def upload_to_gcs(text: str):
    client = storage.Client()
    bucket = client.bucket(settings.GCP_BUCKET)

    date = datetime.utcnow()

    blob = bucket.blob(f"tweets_{date.strftime('%Y-%m-%d')}_{uuid4()}.jsonl")
    blob.upload_from_string(text)
