from utils.llm import llm_4i
from utils.create_agent import create_agent, agent_node
from utils.long_term_memory import LongTermMemory
from langchain import hub



def create_resume_agent(state):
    state_aware_tools = [
    ]
  


def resume_node(state):
    agent = create_resume_agent(state)
    return agent_node(state, agent=agent, name="Resume_Agent")

