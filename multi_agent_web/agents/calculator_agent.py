
from util.tools import current_timestamp,make_msg

def agent4_task(message):
    """Local Calculator"""
    try:
        result = eval(message['content'], {"__builtins__": {}})
    except Exception as e:
        result = f"Error: {e}"

    return make_msg(
        sender="agent4_calculator",
        receiver="orchestrator",
        task="return_calculation",
        content={"result": str(result), "timestamp": current_timestamp()},
        step=2
    )