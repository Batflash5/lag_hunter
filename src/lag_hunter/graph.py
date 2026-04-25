from langgraph.graph import StateGraph, START, END
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from src.lag_hunter.state import HunterState
from src.lag_hunter.agents.planner import run_planner
from src.lag_hunter.agents.locksmith import run_locksmith
from src.lag_hunter.agents.detective import run_detective
from src.lag_hunter.agents.reporter import run_reporter
from src.lag_hunter.utils.router import route_after_analysis


graph = StateGraph(HunterState)
graph.add_node("planner",run_planner)
graph.add_node("locksmith",run_locksmith)
graph.add_node("detective",run_detective)
graph.add_node("reporter",run_reporter)

graph.add_edge(START, "planner")
graph.add_edge("planner", "locksmith")
graph.add_edge("locksmith", "detective")

graph.add_conditional_edges("detective",route_after_analysis,{"planner":"planner","reporter":"reporter"})

graph.add_edge("reporter", END)

conn = sqlite3.connect("lag_hunter_history.db", check_same_thread=False)
memory = SqliteSaver(conn)

app = graph.compile(checkpointer=memory)

with open("hunter_graph_flow.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())