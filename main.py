import os
import shutil
from threading import local
import requests
import csv
import json
from export.local import local
from export.gcp import gcp

apiHost = os.getenv("API_HOST", None)
numGpus= os.getenv("NUM_GPUS", "1")
numTrainEpochs= os.getenv("NUM_TRAIN_EPOCS", "1")
gradientAccumulationSteps = os.getenv("PER_DEVICE_TRAIN_BATCH_SIZE", "1")
perDeviceTrainBatchSize = os.getenv("PER_DEVICE_TRAIN_BATCH_SIZE", "2")
splitTrainingRatio = float(os.getenv("SPLIT_TRAINING_RATIO", "0.9"))

def update(finetuneId, state):
    url = "{}/api/finetunes/{}".format(apiHost,finetuneId)
    requests.put(url, headers={ "accept": "application/json", "Content-Type": "application/json" }, data=json.dumps({ "state": state }))
    
def fetch():
    fetchUrl = "{}/api/finetunes?state=created".format(apiHost)
    fetchJobs = requests.get(fetchUrl).json()
    if fetchJobs is not None and len(fetchJobs) > 0:
        job = fetchJobs[0] 
        if job is not None:
            finetuneId = job["finetuneId"]
            state = "fetched"
            update(finetuneId, state)
        return job
    else:
        return None

def splitTrainValidation(text, splitTrainingRatio):
    lineBreak = "\n"
    splitIndex = -1
    splitLine = int(splitTrainingRatio*text.count(lineBreak))
    for line in range(splitLine):
        splitIndex = text.find(lineBreak, splitIndex + 1)
    train = text[0:splitIndex]
    validation = text[splitIndex:-1]
    return train, validation

def getBaseModel(baseModelId):
    if baseModelId.lower() == "gpt-neo-125m":
        return "EleutherAI/gpt-neo-125M"
    elif baseModelId.lower() == "gpt-neo-1.3b":
        return "EleutherAI/gpt-neo-1.3B"
    elif baseModelId.lower() == "gpt-neo-2.7b":
        return "EleutherAI/gpt-neo-2.7B"
    elif baseModelId.lower() == "gpt-j-6b":
        return "EleutherAI/gpt-j-6B"
    elif baseModelId.lower() == "gpt-neox-20b":
        return "EleutherAI/gpt-neox-20b"
    else:
        return None
     
    
def getStoryIds(storyIds, storyTags):
    tags = ",".join(storyTags)
    listStoryUrl = "{}/api/stories?tags={}".format(apiHost, tags)
    stories = requests.get(listStoryUrl).json()
    for story in stories:
        storyIds.append(story["storyId"])
    storyIds = list(set(storyIds))
    return storyIds

def downloadStories(finetuneDirectory, storyIds, storyTags, splitTrainingRatio):
    storyIds = getStoryIds(storyIds=storyIds, storyTags=storyTags)
    text = ""
    for storyId in storyIds:
        getStoryUrl = "{}/api/stories/{}".format(apiHost, storyId)
        story = requests.get(getStoryUrl).json()
        if story is not None:
            text = text + story["text"] + "\n"
    train, validation = splitTrainValidation(text, splitTrainingRatio)
    trainFile = "{}/train.csv".format(finetuneDirectory)
    validationFile = "{}/validation.csv".format(finetuneDirectory)
    with open(trainFile, mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'text': train})
    with open(validationFile.format(finetuneDirectory), mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'text': validation})
    return trainFile, validationFile

def assign(job):
    if job is not None:
        finetuneId = job["finetuneId"]
        finetuneDirectory = "jobs/{}".format(finetuneId)
        if os.path.exists(finetuneDirectory):
            shutil.rmtree(finetuneDirectory) 
        os.mkdir(finetuneDirectory)
        storyIds = job["storyIds"]
        storyTags = job["storyTags"]
        baseModel = getBaseModel(job["baseModelId"])
        if baseModel is not None:
            trainFile, validationFile = downloadStories(finetuneDirectory, storyIds, storyTags, splitTrainingRatio)
            return baseModel, finetuneId, trainFile, validationFile
    return None, None, None, None

def save(finetuneId, outputDirectory, modelDirectory):
    saved = local.save(outputDirectory,modelDirectory)
    if saved == True:
        update(finetuneId, state = "saved")

def export(finetuneId, modelDirectory):
    exported = gcp.save(modelDirectory)
    if exported == True:
        update(finetuneId, state = "exported")
          
def train(numGpus, baseModel, trainFile, validationFile, outputDirectory, numTrainEpochs, gradientAccumulationSteps, perDeviceTrainBatchSize):
    command ='''deepspeed --num_gpus={} train.py \
    --deepspeed ds_config.json \
    --model_name_or_path {} \
    --train_file {} \
    --validation_file {} \
    --do_train \
    --do_eval \
    --fp16 \
    --overwrite_cache \
    --evaluation_strategy="steps" \
    --output_dir {} \
    --num_train_epochs {} \
    --eval_steps 15 \
    --gradient_accumulation_steps {} \
    --per_device_train_batch_size {} \
    --use_fast_tokenizer False \
    --learning_rate 5e-06 \
    --warmup_steps 10'''.format(numGpus, baseModel, trainFile, validationFile, outputDirectory, numTrainEpochs, gradientAccumulationSteps, perDeviceTrainBatchSize)
    print("Running Training Job........................")
    print(command)
    os.system(command)
    
def run():
    job = fetch()
    baseModel, finetuneId, trainFile, validationFile = assign(job)
    try:
        if baseModel is not None and finetuneId is not None and trainFile is not None and validationFile is not None:
            outputDirectory = "jobs/{}/output".format(finetuneId)
            train(numGpus=numGpus, baseModel=baseModel, trainFile=trainFile, validationFile=validationFile, outputDirectory=outputDirectory, numTrainEpochs=numTrainEpochs, gradientAccumulationSteps=gradientAccumulationSteps, perDeviceTrainBatchSize=perDeviceTrainBatchSize)
            update(finetuneId, state = "completed")
            modelDirectory = "models/{}".format(finetuneId)
            save(finetuneId, outputDirectory, modelDirectory)
            export(job, modelDirectory)
    except:
        update(finetuneId, state = "failed")

def main():
    if apiHost is not None:
        while True:
            run()
    else:
        print("The environment variable for apiHost has not been assigned yet")

if __name__ == "__main__":
    main()

