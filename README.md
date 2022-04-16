# superinsight-trainer-gpt
This is a python application that continuously look for finetunes to train by calling the [SuperInsight FineTuning API](https://github.com/superinsight/superinsight-api-finetunin). After traning has been completed the model can be exported to GCP bucket defined by your environment variable.

# Prerequisite for running the trainer

1. The [SuperInsight FineTuning API](https://github.com/superinsight/superinsight-api-finetuning) is setup and running, assign url under `API_HOST` in the environment variable
2. Include all the environment variables so the trainer can pull jobs from the API and train successfully
3. Host the application on a machine with GPU, depending on which base model you are using, different GPU might be required

## Environment Variables 
Variable | Usage | Required | Default
--- | --- | --- | ---
API_HOST | The API host that is used | True | None
NUM_GPUS | The number of GPUs used to train each job | True | 1
NUM_TRAIN_EPOCS | The number of epochs to train for each job | True | 1
PER_DEVICE_TRAIN_BATCH_SIZE | gradientAccumulationSteps used to train each job | True | 1
PER_DEVICE_TRAIN_BATCH_SIZE | perDeviceTrainBatchSize used to train each job | True | 2
EXPORT_GCP_STORAGE_BUCKET | If you like to export models to GCP bucket, include the bucket name here | False | None
EXPORT_GCP_STORAGE_FOLDER | If you like to export models to GCP bucket, include the bucket name here | False | None


## Available Base Models
Base Model ID | Hardware Tested On | Summary
--- | --- | ---
gpt-neo-125m | NVIDIA V100 GPU [1-8] | This is the `EleutherAI/gpt-neo-125M` model. Great option for testing
gpt-neo-1.3b | NVIDIA V100 GPU [1-8] | This is the `EleutherAI/gpt-neo-1.3B` model. No longer supported by EleutherAI
gpt-neo-2.7b  | NVIDIA V100 GPU [1-8] | This is the `EleutherAI/gpt-neo-2.7B` model. No longer supported by EleutherAI
gpt-j-6b | NVIDIA V100 GPU [1-8] | This is the `EleutherAI/gpt-j-6B` model. Great for finetuning
gpt-neox-20b | N/A  | This is the `EleutherAI/gpt-neox-20b` model. Largest model from EletherAI yet. Having fully been tested with the code in this repo