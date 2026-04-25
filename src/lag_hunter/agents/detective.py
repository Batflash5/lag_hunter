import logging
from langchain_core.messages import AIMessage
from src.lag_hunter.state import HunterState
from src.lag_hunter.tools.stats import calculate_metrics
from src.lag_hunter.tools.plotting import generate_drift_plots


def run_detective(hunterstate: HunterState):
    t1, t2, t3, t4 = hunterstate["t1"], hunterstate["t2"], hunterstate["t3"], hunterstate["t4"]
    avg_delay, avg_offset, std_dev = calculate_metrics(t1, t2, t3, t4)
    
    plot_path = generate_drift_plots(t1, t2, t3, t4)
    # A simple Data Science heuristic: 
    # High jitter (std_dev) relative to delay reduces confidence.
    if avg_delay > 0:
        # We penalize the score if the jitter is high
        score = max(0.0, min(1.0, 1.0 - (std_dev / avg_delay)))
    else:
        score = 0.0

    analysis_msg = (
        f"Detective Analysis Complete.\n"
        f"- Samples took: {len(t1)}"
        f"- Avg Offset: {avg_offset*1000:.2f}ms\n"
        f"- Network Jitter (StdDev): {std_dev*1000:.2f}ms\n"
        f"- Confidence Score: {score:.2f}\n"
        f"Plot saved to: {plot_path}"
    )

    reasoning = (
        f"Detective calculated jitter as {std_dev*1000:.2f}ms. "
        f"Since jitter is { (std_dev/avg_delay)*100 if avg_delay > 0 else 0 } % of the total delay, "
        f"the confidence score was set to {score:.2f}."
    )

    return {
        "average_delay": avg_delay,
        "calculated_offset": avg_offset,
        "confidence_history": [score],
        "messages": [AIMessage(content=analysis_msg)],
        "reasoning_chain": [reasoning]
    }