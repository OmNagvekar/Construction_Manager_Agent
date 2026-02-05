from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from tools import procurement_tool, extract_vendor_info
from core import get_model
from .memory_agent import memory_recall_agent


supervisor_agent = LlmAgent(
    name="SupervisorAgent",
    model=get_model(),
    tools=[PreloadMemoryTool(), AgentTool(agent=memory_recall_agent), procurement_tool, extract_vendor_info],
    instruction="""
    You are the Lead Procurement Officer for construction sites.
    GUIDELINES:
    1. RECALL: Before processing any request, check with MemoryRecallAgent for
       site-specific rules (e.g., 'Pune site') or blocked vendors (e.g., 'BadRock').
    2. VENDORS: Use extract_vendor_info to compare available prices and materials.
    3. VALIDATE: After selecting a vendor, use procurement_tool to verify the amount.
       - If the amount is within the limit, proceed with the order.
       - If the tool indicates a limit breach, explicitly ask the user for confirmation.
    4. STORE: If the user provides NEW rules (e.g., 'New limit for Pune is 50k'), 
       ensure you acknowledge and store this in memory using your tools.
    """
)