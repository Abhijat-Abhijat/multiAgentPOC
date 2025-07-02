import uuid
import time
from typing import Dict
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, ".env")

# Check if .env exists and load it
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")

# === Constants ===
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("Hugging Face API key not found. Please set HF_API_KEY in your .env file.")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}
CODE_MODEL_NAME = "Salesforce/codegen-350M-mono"

# === Load Code Model & Tokenizer ===
code_tokenizer = AutoTokenizer.from_pretrained(CODE_MODEL_NAME)
code_model = AutoModelForCausalLM.from_pretrained(CODE_MODEL_NAME)
code_model.eval()

# === Utilities ===
def current_timestamp() -> str:
    """Returns the current UTC timestamp in ISO 8601 format."""
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')

def message_bus(message: Dict) -> Dict:
    """Simple passthrough message bus function (can be extended)."""
    return message

def generate_code(prompt: str, max_tokens: int = 512) -> str:
    """Generates code using the CodeGen model based on the given prompt."""
    inputs = code_tokenizer(prompt, return_tensors="pt")
    outputs = code_model.generate(
        inputs["input_ids"],
        max_length=inputs["input_ids"].shape[1] + max_tokens,
        do_sample=True,
        temperature=0.7,
        pad_token_id=code_tokenizer.eos_token_id
    )
    return code_tokenizer.decode(outputs[0], skip_special_tokens=True)

def make_msg(sender:str , receiver: str, task: str, content: str, step: int) -> Dict:
    """Formats and returns a standardized message dictionary."""
    return message_bus({
        "id": str(uuid.uuid4()),
        "sender": sender,
        "receiver": receiver,
        "task": task,
        "content": content,
        "metadata": {
            "step": step,
            "timestamp": current_timestamp()
        }
    })
