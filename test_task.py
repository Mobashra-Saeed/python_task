import copy
import task


def make_order(items, status="paid", customer="Ali"):
    return {
        "order_id": "TEST001",
        "customer": customer,
        "items": items,
        "payment_status": status
    }


def test_bad_order_is_rejected_without_changing_stock():
    products = copy.deepcopy(task.products)
    order = make_order([
        {"product_id": "P001", "quantity": 1},
        {"product_id": "P999", "quantity": 1}
    ])

    result = task.process_order(order, products)

    assert result["valid"] is False
    assert result["revenue"] == 0
    assert products["P001"]["stock"] == 10


def test_bad_quantities_and_empty_order_are_rejected():
    products = copy.deepcopy(task.products)

    for quantity in (0, -1, "2", None, True, 11):
        order = make_order([{"product_id": "P001", "quantity": quantity}])
        result = task.process_order(order, products)
        assert result["valid"] is False

    empty_order = make_order([])
    assert task.process_order(empty_order, products)["valid"] is False


def test_invalid_payment_and_empty_inventory_are_rejected():
    products = copy.deepcopy(task.products)
    order = make_order(
        [{"product_id": "P001", "quantity": 1}],
        status="PAID"
    )
    assert task.process_order(order, products)["valid"] is False

    order = make_order([{"product_id": "P001", "quantity": 1}])
    assert task.process_order(order, {})["valid"] is False


def test_stock_is_updated_only_for_paid_valid_orders():
    products = copy.deepcopy(task.products)
    pending_order = make_order(
        [{"product_id": "P001", "quantity": 1}],
        status="pending"
    )
    pending = task.process_order(pending_order, products)

    assert pending["revenue"] == 0
    assert pending["discount"] == 0
    assert pending["shipping"] == 0
    assert products["P001"]["stock"] == 10

    paid_order = make_order([{"product_id": "P001", "quantity": 10}])
    paid = task.process_order(paid_order, products)

    assert paid["valid"] is True
    assert paid["revenue"] == 10200
    assert products["P001"]["stock"] == 0
    assert task.get_top_customer([paid]) == ("Ali", 10200)
    assert task.get_top_selling_product([paid]) == (["Laptop"], 10)


def test_later_order_is_rejected_if_stock_has_run_out():
    products = copy.deepcopy(task.products)
    orders = [
        make_order([{"product_id": "P001", "quantity": 10}]),
        make_order(
            [{"product_id": "P001", "quantity": 1}],
            customer="Ahmed"
        )
    ]

    results = task.process_orders(orders, products)

    assert results[0]["valid"] is True
    assert results[1]["valid"] is False
    assert results[1]["revenue"] == 0


def test_customer_totals_and_tied_best_sellers():
    products = copy.deepcopy(task.products)
    orders = [
        make_order([{"product_id": "P002", "quantity": 2}]),
        make_order(
            [{"product_id": "P003", "quantity": 2}],
            customer="Ahmed"
        )
    ]

    results = task.process_orders(orders, products)

    assert task.get_top_customer(results) == ("Ahmed", 150)
    assert task.get_top_selling_product(results) == (["Keyboard", "Mouse"], 2)


def test_discount_and_shipping_rules():
    assert task.calculate_discount(1000) == 150
    assert task.calculate_discount(500) == 50
    assert task.calculate_discount(200) == 10
    assert task.calculate_discount(199) == 0
    assert task.calculate_shipping(500) == 0
    assert task.calculate_shipping(499) == 20
    assert task.calculate_shipping(499, include_shipping=False) == 0


def test_no_low_stock_products_and_empty_results():
    products = copy.deepcopy(task.products)
    for product in products.values():
        product["stock"] = task.Low_stock_limit + 1

    assert task.get_low_stock_products(products) == []
    assert task.get_top_customer([]) == (None, 0)
    assert task.get_top_selling_product([]) == ([], 0)


if __name__ == "__main__":
    test_bad_order_is_rejected_without_changing_stock()
    test_bad_quantities_and_empty_order_are_rejected()
    test_invalid_payment_and_empty_inventory_are_rejected()
    test_stock_is_updated_only_for_paid_valid_orders()
    test_later_order_is_rejected_if_stock_has_run_out()
    test_customer_totals_and_tied_best_sellers()
    test_discount_and_shipping_rules()
    test_no_low_stock_products_and_empty_results()
    print("All tests passed.")
