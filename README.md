# superinsight-trainer-gpt
This is a python application that continuously look for finetunes to train by calling the [SuperInsight FineTuning API](https://github.com/superinsight/superinsight-api-finetuning). After traning has been completed the model can be exported to GCP bucket defined by your environment variable.

# Prerequisite for running the trainer

1. The [SuperInsight FineTuning API](https://github.com/superinsight/superinsight-api-finetuning) is setup and running, assign url under `API_HOST` in the environment variable
2. Include all the environment variables so the trainer can pull jobs from the API and train successfully
3. Host the application on a machine with GPU, depending on which base model you are using, different GPU might be required
4. To customize your wandb options, use the `WANDB_` variables below or use the ones listed on [wandb](https://docs.wandb.ai/guides/track/advanced/environment-variables)

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
GOOGLE_APPLICATION_CREDENTIALS | If you like to export models to GCP bucket, you will need to include your credentials | False | None
WANDB_API_KEY | The API Key for wandb | False | None
WANDB_NAME | The run name for wandb | False | None
WANDB_NOTES | Notes for wandb  | False | None
WANDB_ENTITY | The entity name for wandb  | False | None
WANDB_PROJECT | The project name for wandb  | False | None
WANDB_MODE | wandb mode | False | None
WANDB_DISABLED | Disable wandb | False | True

## Available Base Models
Here is a summary on base models and hardware that has been tested on so far.
Base Model ID | Hardware Tested On | Summary
--- | --- | ---
gpt-neo-125m | NVIDIA V100 GPU | The `EleutherAI/gpt-neo-125M` model. Good option for testing.
gpt-neo-1.3b | NVIDIA V100 GPU | The `EleutherAI/gpt-neo-1.3B` model.
gpt-neo-2.7b | NVIDIA V100 GPU | The `EleutherAI/gpt-neo-2.7B` model.
gpt-j-6b | NVIDIA V100 GPU | The `EleutherAI/gpt-j-6B` model.
gpt-neox-20b | N/A | The `EleutherAI/gpt-neox-20b` model. Haven't tested on this yet.


## Run Trainer with docker [GPU]
```
docker run --rm --gpus all --name superinsight-trainer-gpt superinsight/superinsight-trainer-gpt:latest
```