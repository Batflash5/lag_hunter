import streamlit as st
from src.lag_hunter.graph import app
from langchain_core.messages import HumanMessage
import os

st.set_page_config(page_title="Lag-Hunter-Prime", page_icon="🎯", layout="wide")

st.title("🎯 Lag-Hunter-Prime: NTP Drift Analyzer")
st.markdown("Automated Multi-Agent Clock Synchronization Analysis")

# 1. Sidebar Configuration
with st.sidebar:
    st.header("Mission Parameters")
    target_server = st.text_input("Target NTP Server", value="time.google.com")
    # We allow the user to suggest parameters, but the Planner may override
    st.info("The AI Planner will optimize these based on network conditions.")
    
    if st.button("Clear History"):
        if os.path.exists("lag_hunter_history.db"):
            os.remove("lag_hunter_history.db")
            st.success("Database reset!")

# 2. Main Execution Area
if st.button("🚀 Start Analysis", use_container_width=True):
    # Configuration for persistence
    config = {"configurable": {"thread_id": "user_streamlit_01"}}
    initial_input = {"messages": [HumanMessage(content=f"Check lag on {target_server}")]}
    
    # Containers for live updates
    status_container = st.container()
    reasoning_container = st.expander("🕵️ Agent Reasoning Chain", expanded=True)
    
    with st.spinner("Agents are coordinating..."):
        # We stream the events to show live progress
        for event in app.stream(initial_input, config=config):
            for node_name, state_update in event.items():
                
                # Show Node Activity
                with status_container:
                    st.toast(f"Node {node_name} completed.")
                    if "messages" in state_update:
                        st.chat_message("assistant").write(state_update["messages"][-1].content)
                
                # Show Reasoning History
                if "reasoning_chain" in state_update:
                    with reasoning_container:
                        for thought in state_update["reasoning_chain"]:
                            st.caption(f"💭 {thought}")

    # 3. Final Report Visualization
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Visual Analysis")
        if os.path.exists("drift_report.png"):
            st.image("drift_report.png", use_container_width=True)
    
    with col2:
        st.subheader("Final Verdict")
        # Fetch final state for specific metrics
        final_state = app.get_state(config).values
        st.metric("Calculated Offset", f"{final_state.get('calculated_offset', 0)*1000:.2f} ms")
        st.metric("Avg Network Delay", f"{final_state.get('average_delay', 0)*1000:.2f} ms")