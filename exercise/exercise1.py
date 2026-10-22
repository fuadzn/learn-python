print("Hello Python!")
print("My goal is to become a Data Engineer")
print("I am learning for data processing and ETL/ELT pipeline also all about data engineering")


customer_id = 1001
customer_name = "Fuad"
customer_age = 25
total_spent = 250000
is_active = True

print(f"{customer_name} has spent Rp.{total_spent} and is {is_active} for our platform")


product_name = "Gaming Mouse"
product_price = 250000
quantity_sold = 8
discount_percentage = 10

revenue_before_discount = product_price * quantity_sold
discount = discount_percentage/100 * product_price * quantity_sold
total = revenue_before_discount - discount

print(f"Product : {product_name}")
print(f"Revenue before discount : Rp. {revenue_before_discount}")
print(f"Discount : Rp. {discount}")
print(f"Revenue after discount : Rp. {total}")
