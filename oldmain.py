import requests
import time
import uuid
import json

# === CONFIG ===
HUGGINGFACE_API_KEY = ""  # Get it from https://huggingface.co/settings/tokens
HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}


# === UTIL ===
def current_timestamp():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')


def message_bus(message):
    """Prints communication between agents"""
    print(f"\n🟢 MessageBus [{message['sender']} ➝ {message['receiver']}]:")
    print(json.dumps(message, indent=2))
    return message


# === AGENTS ===
def agent1_task(input_text):
    """Task planner"""
    message = {
        "id": str(uuid.uuid4()),
        "sender": "agent1_planner",
        "receiver": "agent2_summarizer",
        "task": "summarize",
        "content": input_text,
        "metadata": {
            "step": 1,
            "timestamp": current_timestamp()
        }
    }
    return message_bus(message)


def agent2_task(message):
    """Hugging Face summarization"""
    prompt = message['content']
    response = requests.post(
        HF_MODEL_URL,
        headers=HEADERS,
        json={"inputs": prompt}
    )

    if response.status_code == 200:
        summary = response.json()[0]['summary_text']
    else:
        summary = f"[Error]: {response.text}"

    new_message = {
        "id": str(uuid.uuid4()),
        "sender": "agent2_summarizer",
        "receiver": "formatter",
        "task": "format_output",
        "content": summary,
        "metadata": {
            "step": 2,
            "timestamp": current_timestamp()
        }
    }
    return message_bus(new_message)


def formatter_agent(message):
    """Formatter"""
    formatted_output = {
        "summary": message['content'],
        "word_count": len(message['content'].split()),
        "generated_at": current_timestamp()
    }

    final_message = {
        "id": str(uuid.uuid4()),
        "sender": "formatter",
        "receiver": "orchestrator",
        "task": "return_final_output",
        "content": formatted_output,
        "metadata": {
            "step": 3,
            "timestamp": current_timestamp()
        }
    }
    return message_bus(final_message)


# === ORCHESTRATOR ===
def orchestrator(user_input):
    print("🚀 Starting Multi-Agent AI System\n")

    msg1 = agent1_task(user_input)
    msg2 = agent2_task(msg1)
    msg3 = formatter_agent(msg2)

    print("\n✅ Final Output:")
    print(json.dumps(msg3['content'], indent=2))


# === RUN ===
if __name__ == "__main__":
    user_input = """Albert Einstein's theory of relativity includes both the special theory of relativity and the general theory of relativity. 
The special theory applies to all physical phenomena in the absence of gravity. The general theory explains the law of gravitation and its 
relation to other forces of nature. It applies to the cosmological and astrophysical realm, including astronomy."""

    orchestrator(user_input)

