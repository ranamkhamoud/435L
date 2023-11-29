.. SalesService documentation master file, created by sphinx-quickstart.

Welcome to SalesService's documentation!
=========================================

Sales Service API
=================

This module is a Flask application for a Sales Service API. It consists of functions for managing goods, sales transactions, and sales history.

Endpoints
---------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

1. **Home**
   - **URL:** `/`
   - **Method:** `GET`
   - **Description:** Welcome message for the Sales Service API.
   - **Example Response:**
     ```
     "Welcome to the Sales Service API!"
     ```

2. **Display Goods**
   - **URL:** `/display`
   - **Method:** `GET`
   - **Description:** Fetch goods from Inventory Service.
   - **Example Response:**
     .. code-block:: json

        {
          "Goods": [
            {"name": "Laptop", "category": "Electronics", "price": 1000.0, "stock_count": 5},
            {"name": "Smartphone", "category": "Electronics", "price": 500.0, "stock_count": 10}
          ]
        }

3. **Sale Transaction**
   - **URL:** `/sale`
   - **Method:** `POST`
   - **Description:** Perform a sale transaction.
   - **Example Request:**
     .. code-block:: json

        {
          "name": "Laptop",
          "customer_user": "john_doe"
        }
   - **Example Response:**
     .. code-block:: json

        {"message": "Sale successful"}

4. **Sales History**
   - **URL:** `/sales-history/<username>`
   - **Method:** `GET`
   - **Description:** Retrieve sales history for a specific user.
   - **Example Response:**
     .. code-block:: json

        {
          "sales_history": [
            {
              "good": "Laptop",
              "price": 1000.0,
              "time": "2023-01-01 10:00:00"
            }
          ]
        }

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. automodule:: sales.app
    :members:
    :private-members:
