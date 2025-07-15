from utils.llm import llm_4i
from utils.create_agent import create_agent, agent_node
from utils.long_term_memory import LongTermMemory
from langchain import hub



def create_job_agent(state):
    state_aware_tools = [
    ]
  


def job_node(state):
    agent = create_job_agent(state)
    return agent_node(state, agent=agent, name="Job_Agent")

