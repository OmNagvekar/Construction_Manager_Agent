from google.adk.apps import App, ResumabilityConfig
from .supervisor import supervisor_agent
# This configuration is what allows the 'Pause' to exist in the first place
resumability_config = ResumabilityConfig(is_resumable=True)

ConstructionSiteManagerApp = App(
    name="ConstructionSiteManagerAgent",
    root_agent=supervisor_agent,
    resumability_config=resumability_config
)