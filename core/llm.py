from google.adk.models import LiteLlm
from google.adk.models.google_llm import Gemini
from Setting import settings
from typing import Optional

def get_model(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    temperature: float = 0.7,
    **kwargs
):
    """
    Get a chat model instance using Pydantic settings.
    
    Args:
        model_name: Override the LLM_MODEL from settings
        api_key: Override the LLM_API_KEY from settings
        api_base: Override the LLM_BASE_URL from settings
        temperature: Temperature for model responses
        **kwargs: Additional parameters to pass to the model
    
    Returns:
        A ChatLiteLLM instance configured from settings
    """
    
    final_model_name = model_name or settings.llm_model
    final_api_key = api_key if api_key is not None else settings.llm_api_key
    final_api_base = api_base if api_base is not None else settings.llm_base_url
    
    if "gemini" in final_model_name.lower():
        raise RuntimeError(
            f"[GEMINI_VIA_LITELLM] {final_model_name} model should be accessed via LiteLlm. Please Use Gemini(model={final_model_name[7:]})"
        )
    model_config = {
        "model": final_model_name,
        "temperature": temperature,
        **kwargs
    }
    
    # Add optional parameters only if they are not None
    if final_api_key is not None:
        model_config["api_key"] = final_api_key
    
    if final_api_base is not None:
        model_config["api_base"] = final_api_base

    if not final_model_name:
        raise ValueError("Model name must be provided either as an argument or in settings.")
    
    if "gemini" in final_model_name.lower():
        return Gemini(model=final_model_name[7:],**kwargs)
    return LiteLlm(**model_config)