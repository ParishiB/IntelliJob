from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.prompts import PromptTemplate
from tools.redis_db import get_user_id

def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def agent_node(state, agent, name):
    user_id = get_user_id()
    max_retries = 3
    for _ in range(max_retries):
        result = agent.invoke(state)
        if result["output"].strip():
            return {"messages": [AIMessage(content=result["output"], name=name)]}
        
        # If output is empty, reinvoke the agent with a message to respond with real output
        state["messages"].append(AIMessage(content="Please provide a meaningful response."))
    
    # If we've exhausted all retries and still got an empty output, return a default message
    return {"messages": [AIMessage(content="I apologize, but I'm having trouble generating a response. Please try rephrasing your question.", name=name)]}



