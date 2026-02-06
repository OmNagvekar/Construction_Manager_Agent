from google.adk.agents import LlmAgent
from google.adk.tools.load_memory_tool import LoadMemoryTool
from core import get_model
from prompts import MEMORY_AGENT_PROMPT
memory_recall_agent = LlmAgent(
    name="MemoryRecallAgent",
    model=get_model(),
    tools=[LoadMemoryTool()],
    instruction=MEMORY_AGENT_PROMPT
)