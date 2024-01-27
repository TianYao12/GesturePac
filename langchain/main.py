from dotenv import load_dotenv
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.agents import tool, load_tools, initialize_agent, AgentType
import os

load_dotenv(".env")
KEY = os.getenv('COHERE_API_TOKEN')

from langchain_community.chat_models import ChatCohere
from langchain_core.messages import AIMessage, HumanMessage

model = ChatCohere(cohere_api_key=KEY)

# Send a chat message with chat history, note the last message is the current user message
current_message_and_history = [
    HumanMessage(content="knock knock"),
    AIMessage(content="Who's there?"),
    HumanMessage(content="Tank") ]
print(model(current_message_and_history))