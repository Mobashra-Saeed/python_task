Order Processing Program
========================

A small Python program that checks customer orders, updates product stock, and
prints a sales report.

Project files
-------------

`task.py` contains the sample products and orders, order-processing functions,
and report.

`test_task.py` contains checks for valid orders and common problems, such as
unknown products, invalid quantities, and insufficient stock.

Run the program
---------------

Open a terminal in this folder and run:

```text
python task.py
```

The program processes the sample orders and prints the sales report.

Run the checks
--------------

Run:

```text
python test_task.py
```

If the checks pass, the terminal displays `All tests passed.` If a check fails,
Python reports the line that did not match the expected result.

How order processing works
--------------------------

Each order is checked before it is processed. If any product is unknown, a
quantity is invalid, or there is not enough stock, the entire order is
rejected.

For a valid paid order, the program calculates the subtotal, discount,
shipping, and revenue, then reduces the stock. Pending orders do not affect
stock or the money totals.

The report shows order counts, revenue, discounts, shipping, the top customer,
the best-selling product or products, and products with low stock.
