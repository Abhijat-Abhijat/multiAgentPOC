from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "Salesforce/codegen-350M-mono"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

def generate_code(prompt, max_tokens=128):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output = model.generate(input_ids, max_length=input_ids.shape[1] + max_tokens, do_sample=True)
    return tokenizer.decode(output[0], skip_special_tokens=True)


prompt = "# Write a Python function to calculate factorial of n\n# Python 3\n\ndef"
print(generate_code(prompt))
