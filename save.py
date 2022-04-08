from transformers import GPTNeoForCausalLM, AutoModel, AutoTokenizer, AutoModelForCausalLM
SOURCE_PATH = "finefuned"
TARGET_PATH = "models/test"
model_finetuned = AutoModelForCausalLM.from_pretrained(SOURCE_PATH).to('cuda')
model_finetuned.save_pretrained(TARGET_PATH)
tokenizer = AutoTokenizer.from_pretrained(SOURCE_PATH)
tokenizer.save_pretrained(TARGET_PATH)