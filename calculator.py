import argparse
import json
from typing import List, Dict

def process_orders(prices: List[float], tax_rate: float, discount_threshold: float = 500.0) -> Dict[str, float]:
    """
    Transform raw order prices into an aggregated financial summary.
    Applies a 5% bulk discount if the subtotal exceeds the discount_threshold.
    """
    # Filter out invalid negative prices (Data Cleaning)
    valid_prices = [p for p in prices if p >= 0]
    
    subtotal = sum(valid_prices)
    
    # Conditional business logic
    discount = subtotal * 0.05 if subtotal > discount_threshold else 0.0
    taxable_amount = subtotal - discount
    total_tax = taxable_amount * tax_rate
    final_total = taxable_amount + total_tax

    return {
        "order_count": len(valid_prices),
        "subtotal": round(subtotal, 2),
        "discount_applied": round(discount, 2),
        "tax_rate": tax_rate,
        "total_tax": round(total_tax, 2),
        "final_total": round(final_total, 2)
    }

def main():
    # 1. EXTRACT: Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="CLI Order Price Calculator for Data Engineering Foundations"
    )
    parser.add_argument(
        "--prices", 
        nargs="+", 
        type=float, 
        required=True, 
        help="Space-separated list of order prices (e.g., 120.50 85.00 310.25)"
    )
    parser.add_argument(
        "--tax", 
        type=float, 
        default=0.11, 
        help="Tax rate as a decimal (default: 0.11 for 11%%)"
    )

    args = parser.parse_args()

    # 2. TRANSFORM: Run the calculation logic
    summary = process_orders(prices=args.prices, tax_rate=args.tax)

    # 3. LOAD / OUTPUT: Print structured output (JSON format is standard in DE)
    print(json.dumps(summary, indent=4))

if __name__ == "__main__":
    main()