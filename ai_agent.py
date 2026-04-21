# Step1: Setup API keys for Griq and tavily

import os 
import warnings
warnings.filterwarnings("ignore")

GROQ_API_KEY= os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY= os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY= os.environ.get("OPENAI_API_KEY")

# Step2: setup LLM and Tools 

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

search_tool=TavilySearch(max_results=2)

#Step3: setup AI Agent with Search tool Functionality

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt="Act as an AI Chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)

    tools=[TavilySearch(max_results=2)] if allow_search else []

agent=create_react_agent(
    model=groq_llm,
    tools=[search_tool],
    prompt=system_prompt
)
query="tell me about the trends in crypto markets"
state={"messages": query}
response=agent.invoke(state)
messages=response.get("messages")
ai_message=[message.content for message in messages if isinstance(message, AIMessage)]
print(ai_message[-1])

