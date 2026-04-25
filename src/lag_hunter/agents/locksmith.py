from src.lag_hunter.state import HunterState
from src.lag_hunter.tools import ntp_client
from langchain_core.messages import AIMessage

def run_locksmith(hunterstate: HunterState):

    target_server = hunterstate["target_server"]
    sample_size = hunterstate["sample_size"]
    interval = hunterstate["interval"]

    print(f"--- LOCKSMITH: Starting retrieval from {target_server} ---")
    t1_list, t2_list, t3_list, t4_list = ntp_client.retrieve_time(target_server,sample_size,interval)

    reasoning = (
        f"Locksmith: Executed network burst request to {target_server}. "
        f"Successfully captured {len(t1_list)} timestamp packets with a "
        f"{interval}s delay between requests."
    )

    return {
        "t1": t1_list,
        "t2": t2_list,
        "t3": t3_list,
        "t4": t4_list,
        "messages": [AIMessage(content=f"Locksmith: Data collection from {target_server} is complete.")],
        "reasoning_chain": [reasoning]
    }
