from core import settings
import json
from typing import List, Dict, Any, Optional

def extract_vendor_info(
    material: Optional[str] = None,
    min_quantity: Optional[int] = None,
    max_delivery_days: Optional[int] = None,
    sort_by: Optional[str] = None,  # price_per_unit | quality_rating | delivery_days
    sort_order: str = "asc"          # asc | desc
) -> List[Dict[str, Any]]:
    """
    Filter and retrieve vendor material data based on structured agent queries.

    Supports constraint-based filtering (material, quantity, delivery time)
    and optional sorting (price, quality, delivery days). Performs no
    language reasoning; executes deterministic data lookup only.

    Args:
        material: Material name (e.g., "cement", "sand").
        min_quantity: Minimum required available quantity.
        max_delivery_days: Maximum acceptable delivery time (days).
        sort_by: Field to sort by ("price_per_unit", "quality_rating", "delivery_days").
        sort_order: Sort order ("asc" or "desc").

    Returns:
        List of matching vendor-material records.
    """
    with open(settings.vendor_data_dir, "r") as f:
        VENDOR_DATA = json.load(f)
    results = []

    for vendor in VENDOR_DATA["vendors"]:
        for mat_name, mat_data in vendor["materials"].items():

            if material and mat_name != material:
                continue

            if min_quantity and mat_data["available_quantity"] < min_quantity:
                continue

            if max_delivery_days and mat_data["delivery_days"] > max_delivery_days:
                continue

            results.append({
                "vendor_id": vendor["vendor_id"],
                "vendor_name": vendor["name"],
                "material": mat_name,
                **mat_data
            })

    if sort_by:
        reverse = sort_order == "desc"
        results.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)

    return results
