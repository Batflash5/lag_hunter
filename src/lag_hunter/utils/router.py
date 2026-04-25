from src.lag_hunter.state import HunterState

def route_after_analysis(hunterstate: HunterState) -> str:
    """
    Acts as the traffic cop. 
    Returns the NAME of the next node to execute.
    """
    latest_score = hunterstate["confidence_history"][-1]
    print("latest_score: ",latest_score)
    
    if (latest_score < 0.96) and (len(hunterstate["confidence_history"]) < 2):
        print(f"--- ROUTER: Confidence {latest_score:.2f} is too low. Re-planning... ---")
        return "planner"
    
    print(f"--- ROUTER: Confidence {latest_score:.2f} is sufficient. Reporting... ---")
    return "reporter"