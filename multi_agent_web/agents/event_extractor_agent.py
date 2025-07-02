from util.tools import current_timestamp, make_msg

def agent9_task(message):
    text = message["content"]
    events = [{"event": "Placeholder event", "time": "Unknown"}]
    return make_msg(
        sender="agent9_event_extractor",
        receiver="orchestrator",
        task="return_events",
        content={"events": events, "timestamp": current_timestamp()},
        step=2
    )