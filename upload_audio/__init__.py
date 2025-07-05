import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get('file')
        if not file:
            return func.HttpResponse("No file uploaded", status_code=400)

        blob_service_client = BlobServiceClient.from_connection_string(os.environ["AZURE_STORAGE_CONNECTION_STRING"])
        blob_client = blob_service_client.get_blob_client(container="audio", blob=file.filename)

        blob_client.upload_blob(file.stream, overwrite=True)
        return func.HttpResponse(f"Uploaded {file.filename} successfully", status_code=200)

    except Exception as e:
        logging.error(f"Upload failed: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
