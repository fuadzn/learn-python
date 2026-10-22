# Raw order data
product = "Monitor"
price = 2500000
quantity = 2
shipping_fee = 30000

# Expressions
subtotal = price * quantity
final_price = subtotal + shipping_fee

# Report
print(f"=========== ORDER SUMMARY ===========")
print(f"Product     : {product}")
print(f"Subtotal    : Rp{subtotal:,}")
print(f"Shipping    : Rp{shipping_fee:,}")
print(f"Final Total : Rp{final_price:,}")
print(f"===================================")