from typing import List, Tuple, Optional
import logging
import math


def calculate_metrics(
    t1_list: List[float],
    t2_list: List[float],
    t3_list: List[float],
    t4_list: List[float])->Tuple[Optional[float], Optional[float], Optional[float]]:
    """
    Calculates the delay and offset for the retrieved samples
    """
    delay_lst=[]
    offset_lst=[]
    rtr_samp_sz = len(t4_list)

    if (rtr_samp_sz==0):
        print("No samples provided for metric calculation!!")
        return None, None, None

    for i in range(0,rtr_samp_sz):
        delay = (t4_list[i]-t1_list[i]) - (t3_list[i]-t2_list[i])
        offset = ((t2_list[i]-t1_list[i]) + (t3_list[i]-t4_list[i]))/2
        delay_lst.append(delay)
        offset_lst.append(offset)

    print(f"Calculating metrics for {rtr_samp_sz} samples")
    average_delay = sum(delay_lst)/rtr_samp_sz
    average_offset = sum(offset_lst)/rtr_samp_sz
    variance = sum((x - average_offset) ** 2 for x in offset_lst) / rtr_samp_sz
    std_dev = math.sqrt(variance)

    return average_delay, average_offset, std_dev