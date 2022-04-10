import os


def job(num_gpus, base_model, train_file, validation_file, finetuned_id, num_train_epochs, gradient_accumulation_steps, per_device_train_batch_size):
    command ='''deepspeed --num_gpus={} train.py
    --deepspeed ds_config.json
    --model_name_or_path {}
    --train_file {}
    --validation_file {}
    --do_train
    --do_eval
    --fp16
    --overwrite_cache
    --evaluation_strategy="steps"
    --output_dir jobs\{}\output
    --num_train_epochs {}
    --eval_steps 15
    --gradient_accumulation_steps {}
    --per_device_train_batch_size {}
    --use_fast_tokenizer False
    --learning_rate 5e-06
    --warmup_steps 10
    '''.format(num_gpus, base_model, train_file, validation_file, finetuned_id, num_train_epochs, gradient_accumulation_steps, per_device_train_batch_size)
    print('Running Training Job........................')
    print(command)
    os.system(command)

def main():
  # Call API to look for next job
  # Setup dataset location
  # Setup finetuned location 
  job(num_gpus='1', base_model='EleutherAI/gpt-neo-125M', train_file='datasets/test/train.csv', validation_file='datasets/test/train.csv', finetuned_id='finetuned123', num_train_epochs='1', gradient_accumulation_steps='4', per_device_train_batch_size='8')
        
if __name__ == "__main__":
    main()

