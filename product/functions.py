import json
from decimal import Decimal


def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # Convert Decimal to string
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")