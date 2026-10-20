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

Low_stock_limit= 10


def validate_order(order, products):
    if not isinstance(order, dict):
        return False, "Order must be a dictionary."

    payment_status = order.get("payment_status")
    if payment_status not in ("paid", "pending"):
        return False, "Payment status must be 'paid' or 'pending'."

    if not isinstance(products, dict) or not products:
        return False, "Product inventory is empty."

    items = order.get("items")
    if not isinstance(items, list) or not items:
        return False, "Order has no items."

    requested_quantities = {}
    for item_number, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return False, f"Item {item_number} is invalid."

        product_id = item.get("product_id")
        if not isinstance(product_id, str) or product_id not in products:
            return False, f"Unknown product ID: {product_id}."

        product = products[product_id]
        if not isinstance(product, dict):
            return False, f"Product {product_id} has invalid details."

        quantity = item.get("quantity")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            return False, f"Quantity for product {product_id} must be a positive integer."

        stock = product.get("stock")
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            return False, f"Stock for product {product_id} is invalid."
        requested_quantity = requested_quantities.get(product_id, 0) + quantity
        if requested_quantity > stock:
            return False, f"Insufficient stock for product {product_id}."
        requested_quantities[product_id] = requested_quantity

        price = product.get("price")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            return False, f"Price for product {product_id} is invalid."

    return True, ""


def calculate_order_subtotal(order, products):
    subtotal = 0
    for item in order["items"]:
        product = products[item["product_id"]]
        subtotal += product["price"] * item["quantity"]
    return subtotal


def calculate_discount(subtotal):
    if subtotal >= 1000:
        discount_rate = 0.15
    elif subtotal >= 500:
        discount_rate = 0.10
    elif subtotal >= 200:
        discount_rate = 0.05
    else:
        discount_rate = 0
    return subtotal * discount_rate


def calculate_shipping(subtotal, include_shipping=True):
    if not include_shipping or subtotal >= 500:
        return 0
    return 20


def process_order(order, products, **options):
    unsupported_options = options.keys() - {"include_shipping", "apply_discount"}
    if unsupported_options:
        option_names = ", ".join(sorted(unsupported_options))
        raise TypeError(f"Unsupported option(s): {option_names}")

    include_shipping = options.get("include_shipping", True)
    apply_discount = options.get("apply_discount", True)
    if not isinstance(include_shipping, bool) or not isinstance(apply_discount, bool):
        raise TypeError("include_shipping and apply_discount must be boolean values.")

    status = order.get("payment_status") if isinstance(order, dict) else None
    customer = order.get("customer", "Unknown") if isinstance(order, dict) else "Unknown"
    if customer is None:
        customer = "Unknown"

    is_valid, reason = validate_order(order, products)
    result = {
        "order_id": order.get("order_id", "Unknown") if isinstance(order, dict) else "Unknown",
        "customer": customer,
        "payment_status": status,
        "valid": is_valid,
        "reason": reason,
        "subtotal": 0,
        "discount": 0,
        "shipping": 0,
        "revenue": 0,
        "items": []
    }
    if not is_valid:
        return result

    subtotal = calculate_order_subtotal(order, products)
    result["subtotal"] = subtotal
    result["items"] = [
        {
            "product_id": item["product_id"],
            "product_name": products[item["product_id"]].get(
                "name", item["product_id"]
            ),
            "quantity": item["quantity"]
        }
        for item in order["items"]
    ]

    if status == "paid":
        discount = calculate_discount(subtotal) if apply_discount else 0
        shipping = calculate_shipping(subtotal, include_shipping)
        result["discount"] = discount
        result["shipping"] = shipping
        result["revenue"] = subtotal - discount

        for item in order["items"]:
            product_id = item["product_id"]
            products[product_id]["stock"] -= item["quantity"]

    return result


def process_orders(orders, products, **options):
    return [process_order(order, products, **options) for order in orders]


def sum_amounts(*amounts):
    return sum(amounts)


def get_top_customer(processed_orders):
    paid_orders = [
        result for result in processed_orders
        if result["valid"] and result["payment_status"] == "paid"
    ]
    unique_customers = {result["customer"] for result in paid_orders}
    if not unique_customers:
        return None, 0

    customer_spending = {
        customer: sum_amounts(*(
            result["revenue"] for result in paid_orders
            if result["customer"] == customer
        ))
        for customer in unique_customers
    }
    top_customer, spending = sorted(
        customer_spending.items(),
        key=lambda customer: (-customer[1], str(customer[0]))
    )[0]
    return top_customer, spending


def get_top_selling_product(processed_orders):
    product_sales = {}
    product_names = {}
    for result in processed_orders:
        if result["valid"] and result["payment_status"] == "paid":
            for item in result["items"]:
                product_id = item["product_id"]
                product_names[product_id] = item["product_name"]
                product_sales[product_id] = (
                    product_sales.get(product_id, 0) + item["quantity"]
                )

    if not product_sales:
        return [], 0

    ranked_products = sorted(
        product_sales.items(),
        key=lambda product: (-product[1], product_names[product[0]], product[0])
    )
    highest_quantity = ranked_products[0][1]
    top_products = [
        product_names[product_id] for product_id, quantity in ranked_products
        if quantity == highest_quantity
    ]
    return top_products, highest_quantity


def get_low_stock_products(products):
    low_stock_products = [
        (product_id, details["name"], details["stock"])
        for product_id, details in products.items()
        if details["stock"] <= Low_stock_limit
    ]
    return sorted(low_stock_products, key=lambda product: (product[2], product[1]))


def generate_sales_report(processed_orders, products):
    paid_orders = [
        result for result in processed_orders
        if result["valid"] and result["payment_status"] == "paid"
    ]
    pending_orders = [
        result for result in processed_orders
        if result["valid"] and result["payment_status"] == "pending"
    ]
    rejected_orders = [result for result in processed_orders if not result["valid"]]

    total_revenue = sum_amounts(*(result["revenue"] for result in paid_orders))
    total_discount = sum_amounts(*(result["discount"] for result in paid_orders))
    total_shipping = sum_amounts(*(result["shipping"] for result in paid_orders))
    top_customer, customer_spending = get_top_customer(processed_orders)
    top_products, units_sold = get_top_selling_product(processed_orders)

    print(" SALES REPORT ")
    print(f"Total Orders: {len(processed_orders)}")
    print(f"Paid Orders: {len(paid_orders)}")
    print(f"Pending Orders: {len(pending_orders)}")
    print(f"Rejected Orders: {len(rejected_orders)}")
    print()
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Total Discount: ${total_discount:.2f}")
    print(f"Total Shipping: ${total_shipping:.2f}")
    print()
    if top_customer is None:
        print("Top Customer: None")
    else:
        print(f"Top Customer: {top_customer} (${customer_spending:.2f})")
    if top_products:
        print(f"Top Selling Product: {', '.join(top_products)} ({units_sold} units)")
    else:
        print("Top Selling Product: None")
    print()
    print("Low Stock Products:")
    low_stock_products = get_low_stock_products(products)
    if low_stock_products:
        for product_id, name, stock in low_stock_products:
            print(f"- {name} {product_id}: {stock} remaining")
    else:
        print(" No low-stock products")



def main():
    current_products = {
        product_id: details.copy()
        for product_id, details in products.items()
    }
    processed_orders = process_orders(orders, current_products)
    generate_sales_report(processed_orders, current_products)


if __name__ == "__main__":
    main()
