# LAG-HUNTER-PRIME

## Project Overview
Lag-Hunter-Prime is an agent-based orchestration system designed to measure and analyze clock drift between your local system and global NTP servers. It uses autonomous reasoning to ensure that data collection is reliable even in noisy network environments.

## The Agent Team
1. **Planner**: Interprets user requests and manages the retry logic.
2. **Locksmith**: Connects to time servers and pulls raw data.
3. **Detective**: Calculates statistics like jitter and offset.
4. **Reporter**: Creates the final summary and visualization.

## Key Technical Features
- **Self-Healing Loop**: If data quality is low (Confidence < 0.95), the AI automatically re-plans the mission with more robust settings.
- **Persistent Memory**: Uses a SQLite database to remember every query and reasoning step.
- **Model Agnostic**: Works with NVIDIA NIM, OpenAI, and Gemini.

## Quick Start
1. Install dependencies: `pip install langgraph langchain-nvidia-ai-endpoints python-dotenv matplotlib`.
2. Add your API key to a `.env` file.
3. Run `python main.py`.
4. Optional - You can also Run `streamlit run app.py` to for the streamlit app which runs the same script

## Files Generated
- `drift_report.png`: A visual chart of your clock's drift over time.
- `lag_hunter_history.db`: A complete audit trail of the AI's thoughts and actions.
