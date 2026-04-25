from typing import Annotated, List, Optional, TypedDict
from langchain_core.messages import BaseMessage

import operator

class HunterState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    # Target Server and Sample Size
    target_server: str
    sample_size: int
    interval: float
    # The 4 timestamps required for the analysis
    t1: List[float] # Local Time at which the request sent to server
    t2: List[float] # Server received time
    t3: List[float] # Server Time when it sends response back
    t4: List[float] # Local Time when received
    # Calculated metrics using the retrieved NTP timestamps
    average_delay: Optional[float]
    calculated_offset: Optional[float]
    drift_slope: Optional[float]
    confidence_history: Annotated[List[float], operator.add]
    reasoning_chain: Annotated[List[str], operator.add]