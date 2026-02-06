from google.adk.agents import LlmAgent
from tools import amount_confirmation_tool, extract_vendor_info
from core import get_model
from tools import save_site_rules
from prompts import SYSTEM_PROMPT


supervisor_agent = LlmAgent(
    name="SupervisorAgent",
    model=get_model(),
    tools=[
        amount_confirmation_tool, 
        extract_vendor_info,
        save_site_rules
    ],
    instruction=SYSTEM_PROMPT
)