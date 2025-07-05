import logging
import os
import azure.functions as func
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        blob_name = req.params.get('filename')
        if not blob_name:
            return func.HttpResponse("Missing 'filename' parameter", status_code=400)

        sas_token = generate_blob_sas(
            account_name=os.environ["AZURE_STORAGE_ACCOUNT_NAME"],
            container_name="audio",
            blob_name=blob_name,
            account_key=os.environ["AZURE_STORAGE_ACCOUNT_KEY"],
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        url = f"https://{os.environ['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net/audio/{blob_name}?{sas_token}"
        return func.HttpResponse(url, status_code=200)

    except Exception as e:
        logging.error(f"SAS generation failed: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
