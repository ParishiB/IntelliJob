
from langgraph.graph import END, StateGraph, START
from agents.supervisor_agent import supervisor_agent
from agents.default_agent import default_node
from agents.study_agent import study_node
from agents.job_agent import job_node
from agents.resume_agent import resume_node
from agent_state import AgentState
from langgraph.checkpoint.memory import MemorySaver
import os

members = ["Default_Agent", "Study_Agent", "Job_Agent", "Resume_Agent"]
workflow = StateGraph(AgentState)

workflow.add_node("Default_Agent", lambda state: default_node(state))
workflow.add_node("Study_Agent", lambda state: study_node(state))
workflow.add_node("Job_Agent", lambda state: job_node(state))
workflow.add_node("Resume_Agent", lambda state: resume_node(state))
workflow.add_node("supervisor", supervisor_agent)

for member in members:
    workflow.add_edge(member, "supervisor")

conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)


# Finally, add entrypoint
workflow.add_edge(START, "supervisor")

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# graph_image = graph.get_graph(xray=True).draw_mermaid_png()


# directory = "output"
# file_path = os.path.join(directory, "graph.png")

# if not os.path.exists(directory):
#     os.makedirs(directory)

# with open(file_path, 'wb') as file:
#     file.write(graph_image)


__all__ = ['graph']

