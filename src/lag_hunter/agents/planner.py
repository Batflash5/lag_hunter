from time import time
from src.lag_hunter.state import HunterState

from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from dotenv import load_dotenv

from pydantic import BaseModel, Field


load_dotenv()

class PlanningConfig(BaseModel):
    target_server: str = Field(description="The NTP server to query", default="europe.pool.ntp.org")
    sample_size: int = Field(description="Number of samples to collect", default=20)
    interval: float = Field(description="Seconds to sleep between samples", default=2.0)
    operation_mode: str = Field(description="Whether the current session is NEW_SESSION or RETRY_LOOP", default="NEW_SESSION")
    explanation: str = Field(description="A brief message to the user explaining the plan")
    thought_process: str = Field(description="Internal reasoning for selecting these parameters")

def run_planner(hunterstate:HunterState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.0)
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # llm = ChatNVIDIA(model="nvidia/llama-3.3-nemotron-super-49b-v1.5", temperature=0)
    structured_llm = llm.with_structured_output(PlanningConfig)
    system_prompt = """
        You are the Strategic Planner for 'Lag-Hunter-Prime'. 

        Your objective is to convert the user's natural language request into a specific technical configuration for clock drift analysis.

        LOGIC RULES:
        1. TARGET SERVER: Identify if the user wants to test a specific infrastructure (e.g., 'Google', 'NIST', 'Microsoft'). If they provide a specific URL or IP, use it.
        2. SAMPLE SIZE: If the user indicates they are in a hurry or want a 'quick look', reduce the count. If they mention 'accuracy', 'precision', or 'deep dive', increase it. Do not increase the sample size to more than 35.
        3. INTERVAL: Adjust based on the urgency of the request. Do not increase the interval time to more than 5 seconds.

        OPERATIONAL MODE DETERMINATION
        Your behavior depends strictly on the LAST message in the conversation history:

        1. **NEW_SESSION (Start Case):** - If the history is empty OR the last message is from the 'Reporter' OR the last message is a 'HumanMessage' with a specific server request.
        - ACTION: Follow user instructions exactly. Use defaults, if unspecified.

        2. **RETRY_LOOP (Optimization Case):** - If (and ONLY if) the last message is from the 'Detective' AND mentions a confidence score < 0.95.
        - ACTION: This is a performance failure. You must optimize the NEXT run.
        - RULE: Persist with the SAME target server used in the previous run.
        - RULE: Increase 'sample_size' (MAX 35) and 'interval' (MAX 5s) to combat network jitter.

        ### CRITICAL CONSTRAINTS
        - NEVER assume a past report is just "information." If a Detective failed, you are the recovery mechanism.
        - If the previous run was successful (Reporter message present), reset your logic and wait for a new user command.
        - Do not hallucinate a retry if the previous mission was completed successfully.

        Your output must strictly follow the provided schema. Ensure the 'explanation' field is professional and transparent about the settings you have chosen.
    """
    # history_and_user_input = hunterstate['messages']
    # plan = structured_llm.invoke([
    #     ("system", system_prompt),
    #     ("human", history_and_user_input)
    # ])
    history = hunterstate.get("messages", [])
    messages = [SystemMessage(content=system_prompt)] + history
    plan = structured_llm.invoke(messages)
    print("Operation mode: ",plan.operation_mode)
    if plan.operation_mode=='NEW_SESSION':
        return {
            "target_server": plan.target_server,
            "sample_size": plan.sample_size,
            "interval": plan.interval,
            "confidence_history":[],
            "messages": [AIMessage(content=plan.explanation)],
            "reasoning_chain": [f"Planner: {plan.thought_process}"]
        }
    
    return {
        "target_server": plan.target_server,
        "sample_size": plan.sample_size,
        "interval": plan.interval,
        "messages": [AIMessage(content=plan.explanation)],
        "reasoning_chain": [f"Planner: {plan.thought_process}"]
    }