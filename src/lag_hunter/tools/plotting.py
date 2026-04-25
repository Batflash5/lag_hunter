import matplotlib.pyplot as plt
import numpy as np
import os
from typing import List

def generate_drift_plots(
    t1_list: List[float],
    t2_list: List[float],
    t3_list: List[float],
    t4_list: List[float],
    output_path: str = "drift_report.png"
) -> str:
    """
    Generates a visualization of clock offset and jitter across the sample burst.
    Returns the file path of the saved image.
    """
    if not t1_list:
        return "No data available to plot."

    offsets = []
    delays = []
    for i in range(len(t1_list)):
        off = ((t2_list[i] - t1_list[i]) + (t3_list[i] - t4_list[i])) / 2
        dly = (t4_list[i] - t1_list[i]) - (t3_list[i] - t2_list[i])
        offsets.append(off * 1000)
        delays.append(dly * 1000)

    samples = np.arange(len(offsets))

    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:blue'
    ax1.set_xlabel('Sample Number')
    ax1.set_ylabel('Offset (ms)', color=color)
    ax1.scatter(samples, offsets, color=color, label='Sample Offset', alpha=0.6)
    
    if len(samples) > 1:
        z = np.polyfit(samples, offsets, 1)
        p = np.poly1d(z)
        ax1.plot(samples, p(samples), "r--", label=f"Drift Trend ({z[0]:.4f} ms/sample)")

    ax2 = ax1.twinx()
    color = 'tab:gray'
    ax2.set_ylabel('Network Delay (ms)', color=color, alpha=0.4)
    ax2.plot(samples, delays, color=color, linestyle=':', alpha=0.3, label='Network Delay')

    plt.title('Lag-Hunter-Prime: Clock Drift & Network Jitter Analysis')
    ax1.grid(True, linestyle='--', alpha=0.7)
    fig.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return os.path.abspath(output_path)