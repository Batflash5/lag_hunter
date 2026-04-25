from src.lag_hunter.graph import app
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "user_01"}}

user_input = {"messages": [HumanMessage(content="I want to know the lag from my system to google time. Take 30 samples")]}

print("--- STARTING: LAG-HUNTER-PRIME ---")

final_state = {}

for event in app.stream(user_input, config=config):
    for node_name, state_update in event.items():
        print(f"\n[Node: {node_name}]")
        if "messages" in state_update:
            print(f"Status: {state_update['messages'][-1].content}")
        final_state = state_update

snapshot = app.get_state(config)
full_reasoning = snapshot.values.get("reasoning_chain", [])

print("\n" + "="*30)
print("--- FINAL AGENT REASONING CHAIN ---")
print("="*30)

if full_reasoning:
    for thought in full_reasoning:
        print(f"-> {thought}")
else:
    print("No reasoning recorded.")