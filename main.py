from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from src.news_search import search_google_news

# Load API Keys from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

# Initialize CDP AgentKit wrapper
cdp = CdpAgentkitWrapper()

# Create toolkit from wrapper
cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)

# Get all available tools
tools = cdp_toolkit.get_tools()

# Structured Tool for crypto news
crypto_news_tool = StructuredTool.from_function(
    search_google_news,
    name="search_google_news",
    description="Get the latest crypto news, such as: BTC"
)

# Add custom tools
tools.append(crypto_news_tool)

# Create an agent using available tools
agent_executor = create_react_agent(llm, tools)

# Define request model
class UserInput(BaseModel):
    user_input: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods such as GET, POST, OPTIONS
    allow_headers=["*"],  # Allow all necessary headers for communication
)

@app.post("/process_input")
async def process_user_input(request: UserInput):
    """API endpoint to process user input"""
    messages = [HumanMessage(content=request.user_input)]
    
    # Execute the agent with the user input
    events = agent_executor.stream({"messages": messages}, stream_mode="values")

    # Collect responses
    responses = []
    for event in events:
        responses.append(event["messages"][-1].content)

    return {"responses": responses}

# Run command
# uvicorn main:app --reload
