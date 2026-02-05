from google.adk.agents import LlmAgent
from google.adk.tools.load_memory_tool import LoadMemoryTool
from core import get_model

memory_recall_agent = LlmAgent(
    name="MemoryRecallAgent",
    model=get_model(),
    tools=[LoadMemoryTool()],
    instruction="""
    You are an agent specializes in recalling
    information regarding site rules and information from the construction project memory database."""
)