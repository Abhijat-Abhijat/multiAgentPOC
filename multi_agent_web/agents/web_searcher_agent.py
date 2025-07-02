from util.tools import current_timestamp, make_msg

def agent6_task(message):
    query = message["content"].replace("search:", "").strip()
    result = f"Search results for '{query}' not implemented. Integrate SerpAPI or Bing Search API here."
    return make_msg(
        sender="agent6_web_searcher",
        receiver="orchestrator",
        task="return_search",
        content={"result": result, "timestamp": current_timestamp()},
        step=2
    )
