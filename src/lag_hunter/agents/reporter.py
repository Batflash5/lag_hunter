from src.lag_hunter.state import HunterState

from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from dotenv import load_dotenv


load_dotenv()

def run_reporter(hunterstate: HunterState):
    recent_conf_score = hunterstate['confidence_history'][-1]
    final_offset = hunterstate['calculated_offset']
    final_delay = hunterstate['average_delay']

    full_reasoning = "\n".join(hunterstate["reasoning_chain"])

    technical_results = f"""
    TECHNICAL FINDINGS:
    - Final Offset: {final_offset*1000:.2f} ms
    - Average Delay: {final_delay*1000:.2f} ms
    - Confidence Score: {recent_conf_score:.2f}
    - Visual Report: 'drift_report.png' has been generated.

    COMPLETE INTERNAL REASONING
    {full_reasoning}
    """
    system_prompt = """
        You are the Reporter for 'Lag-Hunter-Prime'. 

        Your task is to provide a final, professional verdict on the user's clock synchronization.
    
        TONE: Professional, analytical, and helpful.

        GUIDELINES:
            - If the offset is positive, the user's clock is AHEAD.
            - If the offset is negative, the user's clock is BEHIND.
            - Mention if the confidence score suggests the results are definitive or if they should be taken with a grain of salt due to network jitter.
            - Explicitly mention that 'drift_report.png' contains the visual proof.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=1.0)
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # llm = ChatNVIDIA(model="nvidia/llama-3.3-nemotron-super-49b-v1.5", temperature=0)
    response = llm.invoke([
        ('system', system_prompt),
        ('human', technical_results)
    ])

    return {
        'messages': [AIMessage(content=response.content)],
        'reasoning_chain': ["Reporter: Finalized the mission report."]
    }