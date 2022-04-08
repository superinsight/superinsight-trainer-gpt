from google.cloud import storage
import pathlib
import os

def upload_model(sourcePath, bucketName, bucketFolder):
  directory = str(pathlib.Path().resolve()) + '/' + sourcePath
  for file in os.listdir(directory):
      filename = os.fsdecode(file)
      dest = "{}/{}".format(bucketFolder, filename)
      upload_file(os.path.join(directory, filename), bucketName, dest)

def upload_file(source, bucketName, bucketDestination):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucketName)
    blob = bucket.blob(bucketDestination)
    blob.upload_from_filename(source)
    print(
        "File {} uploaded to {}.".format(
            source, bucketDestination
        )
    )
#upload_model("models/test","gcp-storage-bucket","test");
