import ntplib
import logging
from time import ctime, sleep


def retrieve_time(target_server:str, sample_size:int, interval: float):
    """
    Retrieves a burst of NTP timestamps
    """
    c = ntplib.NTPClient()
    t1_list, t2_list, t3_list, t4_list = [],[],[],[]

    for i in range(0,sample_size):
        if i:
            sleep(interval)
        try:
            response = c.request(target_server,version=3)
            t1_list.append(response.orig_timestamp)
            t2_list.append(response.recv_timestamp)
            t3_list.append(response.tx_timestamp)
            t4_list.append(response.dest_timestamp)
            print(f"Retrieving sample {i+1}")

        except Exception as e:
            print(f"NTP Request failed for sample {i}: {e}")
            continue

    print(f"Successfully retrieved {len(t1_list)} samples")

    return t1_list, t2_list, t3_list, t4_list
