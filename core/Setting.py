from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SystemSettings(BaseSettings):
    """
    System configuration settings loaded from environment variables.
    
    Environment Variables:
        LLM_MODEL: Model name (required)
        LLM_API_KEY: API key for the provider (optional)
        LLM_BASE_URL: Base URL/endpoint for the API (optional)
    """
     
    llm_model: Optional[str] = Field(
        default="gemini/gemini-2.5-flash",
        description="Model name with provider prefix (e.g., 'groq/llama-3.1-70b-versatile')"
    )
    llm_api_key: Optional[str] = Field(
        default=None,
        description="API key for the provider"
    )
    llm_base_url: Optional[str] = Field(
        default=None,
        description="Base URL/endpoint for the API"
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator('llm_base_url')
    @classmethod
    def validate_base_url(cls, v):
        """Set empty strings to None"""
        if v == "":
            return None
        return v
    
    @field_validator('llm_api_key')
    @classmethod
    def validate_api_key(cls, v):
        """Set empty strings to None"""
        if v == "":
            return None
        return v


settings = SystemSettings()