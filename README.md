# superinsight-trainer-gpt
This is a python application that continuously look for finetunes to train by calling the SuperInsight FineTuning API. After traning has been completed the model can be exported to GCP bucket defined by your environment variable.

# Setting up the trainer
Include all the neessary environment variables so the trainer can pull jobs from the API and train successfully

## Environment Variables 
Variable | Usage | Required | Default
--- | --- | --- | ---
API_HOST | The API host that is used | None 
NUM_GPUS | The number of GPUs used to train each job | true | 1
NUM_TRAIN_EPOCS | The number of epochs to train for each job | true | 1
PER_DEVICE_TRAIN_BATCH_SIZE | gradientAccumulationSteps used to train each job | true | 1
PER_DEVICE_TRAIN_BATCH_SIZE | perDeviceTrainBatchSize used to train each job | true | 2
EXPORT_GCP_STORAGE_BUCKET | If you like to export models to GCP bucket, include the bucket name here | false | None
EXPORT_GCP_STORAGE_FOLDER | If you like to export models to GCP bucket, include the bucket name here | false | None