import os


def job():
    command ='''
    deepspeed --num_gpus=1 train.py \
    --deepspeed ds_config.json \
    --model_name_or_path EleutherAI/gpt-neo-125M \
    --train_file datasets/test/train.csv \
    --validation_file datasets/test/validation.csv \
    --do_train \
    --do_eval \
    --fp16 \
    --overwrite_cache \
    --evaluation_strategy="steps" \
    --output_dir finetuned \
    --num_train_epochs 1 \
    --eval_steps 15 \
    --gradient_accumulation_steps 4 \
    --per_device_train_batch_size 8 \
    --use_fast_tokenizer False \
    --learning_rate 5e-06 \
    --warmup_steps 10
    '''
    os.system(command)

def main():
  # Call API to look for next job
  # Setup dataset location
  # Setup finetuned location 
  job()
        
if __name__ == "__main__":
    main()

