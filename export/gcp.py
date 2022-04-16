from google.cloud import storage
import pathlib
import os
bucketName= os.getenv("EXPORT_GCP_STORAGE_BUCKET", None)
bucketFolder= os.getenv("EXPORT_GCP_STORAGE_FOLDER", None)

class gcp:
    def upload_model(sourcePath, bucketName, bucketFolder):
        directory = str(pathlib.Path().resolve()) + '/' + sourcePath
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            dest = "{}/{}".format(bucketFolder, filename)
            gcp.upload_file(os.path.join(directory, filename), bucketName, dest)

    def upload_file(source, bucketName, bucketDestination):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketName)
        blob = bucket.blob(bucketDestination)
        blob.upload_from_filename(source)
        
    def save(sourcePath):
        if bucketName is not None and bucketName is not None:
            gcp.upload_model(sourcePath= sourcePath, bucketName=bucketName, bucketFolder=bucketFolder)
            return True
