from util.tools import current_timestamp, make_msg

def formatter_agent(message):
    """Formatter"""
    formatted = {
        "result": message['content'],
        "word_count": len(message['content'].split()),
        "generated_at": current_timestamp()
    }
    return make_msg(
        sender="formatter",
        receiver="orchestrator",
        task="return_summary",
        content=formatted,
        step=3
    )
