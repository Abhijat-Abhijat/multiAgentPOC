from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from agents.summarizer_agent import summarizer_agent
from agents.calculator_agent import agent4_task
from agents.code_generator_agent import agent5_task
from agents.formatter_agent import formatter_agent
from agents.sentiment_analyzer_agent import agent7_task
from agents.web_searcher_agent import agent6_task
from agents.data_visualizer_agent import agent8_task
from agents.event_extractor_agent import agent9_task
from agents.keyword_extractor_agent import agent10_task

from util.tools import make_msg

# === AGENT DISPATCH LOGIC ===

agent_registry = {
    "agent4_calculator": agent4_task,
    "agent5_code_writer": agent5_task,
    "agent6_web_searcher": agent6_task,
    "agent7_sentiment_analyzer": agent7_task,
    "agent8_data_visualizer": agent8_task,
    "agent9_event_extractor": agent9_task,
    "agent10_keyword_extractor": agent10_task,
}

def agent1_task(user_input):
    user_input = user_input.strip().lower()

    if user_input.startswith("code:"):
        return make_msg("agent1_task","agent5_code_writer", "generate_code", user_input, 2)
    elif user_input.startswith("search:"):
        return make_msg("agent1_task","agent6_web_searcher", "search_web", user_input, 2)
    elif user_input.startswith("sentiment:"):
        return make_msg("agent1_task","agent7_sentiment_analyzer", "analyze_sentiment", user_input, 2)
    elif user_input.startswith("visualize:"):
        return make_msg("agent1_task","agent8_data_visualizer", "generate_chart_data", user_input, 2)
    elif user_input.startswith("events:"):
        return make_msg("agent1_task","agent9_event_extractor", "extract_events", user_input, 2)
    elif user_input.startswith("keywords:"):
        return make_msg("agent1_task","agent10_keyword_extractor", "extract_keywords", user_input, 2)
    elif any(op in user_input for op in "+-*/()"):
        return make_msg("agent1_task","agent4_calculator", "calculate", user_input, 2)
    else:
        return make_msg("agent1_task","summarizer", "summarize", user_input, 2)


# === FASTAPI CONFIGURATION ===

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/run")
async def run_multi_agent(request: Request):
    data = await request.json()
    user_input = data["input"]
    log = []

    msg1 = agent1_task(user_input)
    log.append(msg1)
    receiver = msg1["receiver"]

    if receiver == "summarizer":
        print("Running summarizer agent")
        msg2 = summarizer_agent(msg1)
        log.append(msg2)
        msg3 = formatter_agent(msg2)
        log.append(msg3)
        return JSONResponse(content={"log": log, "final": msg3["content"]})

    elif receiver in agent_registry:
        handler = agent_registry[receiver]
        msg2 = handler(msg1)
        log.append(msg2)
        return JSONResponse(content={"log": log, "final": msg2["content"]})

    return JSONResponse(content={"error": "Unknown route"})
