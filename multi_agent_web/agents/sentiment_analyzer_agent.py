from util.tools import current_timestamp, make_msg
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def agent7_task(message):
    print(f"Sentiment Analysis:")
    analysis = sentiment_pipeline(message["content"])[0]
    return make_msg(
        sender="agent7_sentiment_analyzer",
        receiver="orchestrator",
        task="return_sentiment",
        content={"label": analysis["label"], "score": analysis["score"], "timestamp": current_timestamp()},
        step=2
    )
