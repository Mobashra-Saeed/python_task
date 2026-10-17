products = {
    "P001": {"name": "Laptop", "price": 1200, "category": "Electronics", "stock": 10},
    "P002": {"name": "Mouse", "price": 25, "category": "Accessories", "stock": 50},
    "P003": {"name": "Keyboard", "price": 75, "category": "Accessories", "stock": 20},
    "P004": {"name": "Monitor", "price": 300, "category": "Electronics", "stock": 15}
}

orders = [
    {
        "order_id": "ORD001", "customer": "Ali",
        "items": [
            {"product_id": "P001", "quantity": 1},
            {"product_id": "P002", "quantity": 2}
        ],
        "payment_status": "paid"
    },
    {
        "order_id": "ORD002", "customer": "Ahmed",
        "items": [
            {"product_id": "P003", "quantity": 2},
            {"product_id": "P004", "quantity": 1}
        ],
        "payment_status": "paid"
    },
    {
        "order_id": "ORD003", "customer": "Ali",
        "items": [{"product_id": "P002", "quantity": 5}],
        "payment_status": "pending"
    }
]

def is_item_valid(item, products):
    product_id = item.get("product_id")
    quantity = item.get("quantity", 0)
    
    if not products or product_id not in products:
        return False
    if quantity <= 0:
        return False
    if quantity > products[product_id].get("stock", 0):
        return False
    return True


# 1. Validate Orders
def validate_orders(orders, products):
    if not orders:
        print("No orders to validate.")
        return

    for order in orders:
        items = order.get("items", [])
        if not items:
            print(f"Order {order.get('order_id')} has no items.")
            continue

        for item in items:
            if is_item_valid(item, products):
                print(f"Order {order.get('order_id')}: Product {item.get('product_id')} with Quantity: {item.get('quantity')} is valid.")
            else:
                print(f"Order {order.get('order_id')}: Product {item.get('product_id')} is invalid or out of stock.")


# 2. Calculate Order Subtotal
def price_calc(orders, products):
    subtotals = {}
    total_orders_price = 0

    if not orders:
        print("No orders available to calculate price.")
        return subtotals, 0

    for order in orders:
        order_id = order.get("order_id")
        subtotal = 0
        items = order.get("items", [])

        for item in items:
            if is_item_valid(item, products):
                product_id = item.get("product_id")
                quantity = item.get("quantity", 0)
                subtotal += products[product_id]["price"] * quantity

        subtotals[order_id] = subtotal
        total_orders_price += subtotal
        print(f"Order {order_id} Subtotal: ${subtotal:.2f}")

    print(f"Combined Subtotal Across All Orders: ${total_orders_price:.2f}")
    return subtotals, total_orders_price


# 3. Apply Discounts
def discount_calc(orders, products):
    total_discount = 0
    order_totals = {}

    if not orders:
        return order_totals, 0

    for order in orders:
        order_id = order.get("order_id")
        subtotal = 0

        for item in order.get("items", []):
            if is_item_valid(item, products):
                product_id = item.get("product_id")
                quantity = item.get("quantity", 0)
                subtotal += products[product_id]["price"] * quantity

        if subtotal >= 1000:
            discount_percent = 15
        elif subtotal >= 500:
            discount_percent = 10
        elif subtotal >= 200:
            discount_percent = 5
        else:
            discount_percent = 0

        discount_amount = (subtotal * discount_percent) / 100
        total_discount += discount_amount
        final_price = subtotal - discount_amount

        print(f"Order {order_id} Subtotal: ${subtotal:.2f} with  Discount: {discount_percent}% (${discount_amount:.2f}) has final price: ${final_price:.2f}")
        order_totals[order_id] = final_price

    return order_totals, total_discount


# 4. Calculate Shipping
def shipping_calc(orders, subtotals):
    global total_shipping
    total_shipping = 0
    shipping_charges = {}

    if not orders or not subtotals:
        return shipping_charges, 0

    for order in orders:
        order_id = order.get("order_id")
        subtotal = subtotals.get(order_id, 0)
        status = str(order.get("payment_status", "")).lower()

        if subtotal >= 500:
            charge = 0
        else:
            charge = 20

        if status == "paid":
            total_shipping += charge

        shipping_charges[order_id] = charge
        print(f"Shipping charge for order {order_id} with ${subtotal:.2f} is ${charge}")

    return shipping_charges, total_shipping



# 5. Payment Handling
def revenue_calc(orders, products):
    total_revenue = 0

    if not orders:
        print("No orders available to calculate revenue.")
        return 0

    for order in orders:
        status = str(order.get("payment_status", "")).lower()
        order_id = order.get("order_id")

        if status == "paid":
            order_subtotal = 0
            for item in order.get("items", []):
                if is_item_valid(item, products):
                    product_id = item.get("product_id")
                    quantity = item.get("quantity", 0)
                    order_subtotal += products[product_id]["price"] * quantity

            if order_subtotal >= 1000:
                discount_percent = 15
            elif order_subtotal >= 500:
                discount_percent = 10
            elif order_subtotal >= 200:
                discount_percent = 5
            else:
                discount_percent = 0

            order_subtotal -= (order_subtotal * discount_percent) / 100

            total_revenue += order_subtotal
            print(f"Order {order_id} Paid Total Revenue: ${order_subtotal:.2f}")
        else:
            print(f"Order {order_id} skipped (Payment status: {order.get('payment_status')})")

    print(f"Total completed revenue is ${total_revenue:.2f}")
    return total_revenue


# 6. Update Inventory
def inventory(orders, products):
    if not orders or not products:
        print("No orders or products available for inventory update.")
        return

    for order in orders:
        status = str(order.get("payment_status", "")).lower()
        if status == "paid":
            items = order.get("items", [])
            if all(is_item_valid(item, products) for item in items):
                for item in items:
                    product_id = item.get("product_id")
                    quantity = item.get("quantity", 0)
                    products[product_id]["stock"] -= quantity
                    print(f"Product {product_id} processed. Remaining stock: {products[product_id]['stock']}")
            else:
                for item in items:
                    if not is_item_valid(item, products):
                        print(f"Order {order.get('order_id')}: Product {item.get('product_id')} is invalid or out of stock.")
        else:
            print(f"Order {order.get('order_id')} skipped for inventory update. Status: '{order.get('payment_status')}'")


# 7. Generate Reports
def low_stock(products):
    if not products:
        print("No products available.")
        return {}

    is_low = lambda details: details.get("stock", 0) <= 10
    
    low_stock_items = {}
    for product_id, details in products.items():
        if is_low(details):
            stock = details.get("stock", 0)
            low_stock_items[product_id] = stock
            print(f"{details.get('name', 'Unknown')} ({product_id}) is low in stock: {stock} remaining")

    if not low_stock_items:
        print("No low-stock products found.")

    return low_stock_items


def get_top_customer(orders, products):
    customer_spending = {}

    if not orders:
        return None, 0

    for order in orders:
        status = str(order.get("payment_status", "")).lower()
        if status == "paid":
            customer = order.get("customer", "Unknown")
            order_total = 0

            for item in order.get("items", []):
                if is_item_valid(item, products):
                    product_id = item.get("product_id")
                    quantity = item.get("quantity", 0)
                    order_total += products[product_id]["price"] * quantity

            if order_total >= 1000:
                discount_percent = 15
            elif order_total >= 500:
                discount_percent = 10
            elif order_total >= 200:
                discount_percent = 5
            else:
                discount_percent = 0

            order_total -= (order_total * discount_percent) / 100

            customer_spending[customer] = customer_spending.get(customer, 0) + order_total

    if not customer_spending:
        return None, 0

    top_customer = None
    max_spend = 0
    for customer, spend in customer_spending.items():
        if spend > max_spend:
            max_spend = spend
            top_customer = customer

    return top_customer, max_spend


def get_top_selling_product(orders, products):
    product_sales = {}

    if not orders or not products:
        return None, 0

    for order in orders:
        status = str(order.get("payment_status", "")).lower()
        if status == "paid":
            for item in order.get("items", []):
                if is_item_valid(item, products):
                    product_id = item.get("product_id")
                    quantity = item.get("quantity", 0)
                    product_sales[product_id] = product_sales.get(product_id, 0) + quantity

    if not product_sales:
        return None, 0

    max_quantity = 0
    for quantity in product_sales.values():
        if quantity > max_quantity:
            max_quantity = quantity

    top_products = [
        ", ".join(products[p_id]["name"] for p_id, qty in product_sales.items() if qty == max_quantity)
    ]

    return top_products, max_quantity


def display_orders(orders):
    paid_orders = []
    pending_orders = []
    rejected_orders = []

    if not orders:
        print("No orders to display.")
        return

    for order in orders:
        order_id = order.get("order_id", "Unknown")
        status = str(order.get("payment_status", "")).lower()

        if status == "paid":
            paid_orders.append(order_id)
        elif status == "pending":
            pending_orders.append(order_id)
        else:
            rejected_orders.append(order_id)

    print(f"Total orders: {len(orders)}")
    print(f"Paid orders are: {paid_orders}")
    print(f"Pending orders are: {pending_orders}")
    print(f"Rejected orders are: {rejected_orders}")


validate_orders(orders, products)
subtotals, total_orders_price = price_calc(orders, products)
discounted_totals, total_discount = discount_calc(orders, products)
shipping_calc(orders, subtotals)
total_revenue = revenue_calc(orders, products)
inventory(orders, products)

low_stock(products)

top_customer, spend = get_top_customer(orders, products)
print(f"Top Customer: {top_customer} with total spend of ${spend:.2f}")

top_products, quantity_sold = get_top_selling_product(orders, products)
if top_products:
    print("Top Selling Product:", *top_products, f"with {quantity_sold} units sold") 
else:
    print("No top selling product found.")

display_orders(orders)

print(f"Total Revenue:  ${total_revenue:.2f}")
print(f"Total Discount: ${total_discount:.2f}")
print(f"Total Shipping: ${total_shipping:.2f}")