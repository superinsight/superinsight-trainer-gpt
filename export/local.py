from transformers import GPTNeoForCausalLM, AutoModel, AutoTokenizer, AutoModelForCausalLM

class local:
    def save(sourcePath, targetPath):
        model_finetuned = AutoModelForCausalLM.from_pretrained(sourcePath).to('cuda')
        model_finetuned.save_pretrained(targetPath)
        tokenizer = AutoTokenizer.from_pretrained(sourcePath)
        tokenizer.save_pretrained(targetPath)
        return True