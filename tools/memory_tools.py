import sqlite3
import json
from google.adk.agents import FunctionTool
from utils import db_manager

def save_site_rules(site_name: str, rules_dict: dict):
    """
    Persists site-specific constraints (e.g., limits, banned vendors) to the database.
    Args:
        site_name: The target construction site identifier.
        rules_dict: Dictionary of rules to store as a JSON configuration.
    """
    with db_manager.get_connection() as conn: 
        # We store the whole dictionary as a string
        conn.execute("REPLACE INTO site_configs VALUES (?, ?)", 
                    (site_name.lower(), json.dumps(rules_dict)))

    return f"Rules for {site_name} updated successfully."

def check_approval_limit(site_name: str, amount: float, **kwargs) -> bool:
    """
    Evaluates if an order amount exceeds the site's stored approval limit.
    Args:
        site_name: The target construction site identifier.
        amount: The amount to be checked.
        **kwargs: Additional keyword arguments (not used in this simple implementation).
    Returns:
        True if the amount exceeds the limit (requires human approval), False otherwise.
    """
    with db_manager.get_connection() as conn:
        row = conn.execute("SELECT rules FROM site_configs WHERE site=?", 
                                (site_name.lower(),)).fetchone()

    if row:
        rules = json.loads(row[0]) # Convert string back to Python Dict
        limit = rules.get("limit", float('inf')) # Dynamic lookup
        # Trigger PAUSE if amount (42,000) > limit (40,000)
        return amount > limit 
    return False

def execute_order(site_name:str,material:str,quantity:int,amount:float,**kwargs) -> str:
    """
    A placeholder tool to simulate order execution.
    Args:
        site_name: The name of the construction site.
        material: The material to be ordered.
        quantity: The quantity of the material to be ordered.
        amount: The total amount for the order.
        **kwargs: Additional keyword arguments (not used in this simple implementation).
    
    Returns:
        A confirmation message indicating the order has been executed.
    """
    return {"status": "success", "order": f"{quantity} {material} for {site_name} with amount {amount}"}

amount_confirmation_tool = FunctionTool(
    execute_order,
    require_confirmation=check_approval_limit,
)