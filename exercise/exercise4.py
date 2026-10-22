# Raw data
order_id = 1001
price = 150000
quantity = 0
is_paid = True

# Expressions
can_process = order_id > 0 and price > 0 and quantity > 0 and is_paid == True

# Report
print(f"Can process order {order_id}: {can_process}")