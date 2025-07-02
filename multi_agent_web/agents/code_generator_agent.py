from util.tools import current_timestamp, generate_code, make_msg


def agent5_task(message):
    """Code Writer using local CodeGen"""
    user_prompt = message['content'].replace("code:", "").strip()
    
    prompt = f"'''Write a complete Python script to {user_prompt}'''\n\n# Python 3\n"

    generated = generate_code(prompt, max_tokens=256)

    code_start = generated.find("def ")
    code_output = generated[code_start:] if code_start != -1 else generated

    if not code_output.strip().endswith(('\n', ')', '}', 'return', ':')):
        code_output += "\n# [Note: Output might be incomplete. Try rephrasing your input or increasing max tokens.]"

    return make_msg(
        sender="agent5_code_writer",
        receiver="orchestrator",
        task="return_code",
        content={"code": code_output,
            "timestamp": current_timestamp()},
        step=2
    ) 