
from langchain_core.messages import BaseMessage
from typing import Annotated, Sequence
from typing_extensions import TypedDict
import operator
from langchain_community.chat_message_histories import RedisChatMessageHistory

# Define the structure of the agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    userID: str

