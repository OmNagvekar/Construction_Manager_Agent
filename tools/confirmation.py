from google.adk.agents import FunctionTool

def check_approval_limit(
    limit: float,
    amount: float,
    **kwargs
) -> bool:
    """
    A simple tool to check if an amount is within an approval limit.
    Args:
        limit: The maximum approved amount.
        amount: The amount to be checked.
        **kwargs: Additional keyword arguments (not used in this simple implementation).
    
    Returns:
        True if the amount is within the limit, False otherwise.
    """
    return amount >= limit

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

procurement_tool = FunctionTool(
    execute_order,
    require_confirmation=check_approval_limit,
)