import ast
from util.tools import current_timestamp, make_msg

def agent8_task(message):
    try:    
        print(message["content"])
        content = message["content"].replace("visualize:", "").strip()
        parsed = ast.literal_eval(content)
        if isinstance(parsed, dict):
            summary = [{"label": k, "value": v} for k, v in parsed.items()]
        else:
            summary = "Invalid data format. Provide a dictionary-like input."
    except Exception as e:
        summary = str(e)

    return make_msg(
        sender="agent8_data_visualizer",
        receiver="orchestrator",
        task="return_visualization_data",
        content={"summary": summary, "timestamp": current_timestamp()},
        step=2
    )
