import requests
from util.tools import HEADERS, HF_MODEL_URL, make_msg

def summarizer_agent(message):
    """Summarizer (Hugging Face)"""
    response = requests.post(HF_MODEL_URL, headers=HEADERS, json={"inputs": message['content']})
    summary = response.json()[0]["summary_text"] if response.status_code == 200 else "Error summarizing"
    print(f"Summarization Response: {summary}")
    return make_msg(
        sender="summarizer",
        receiver="formatter",
        task="format_summary",
        content=summary,
        step=2
    )
