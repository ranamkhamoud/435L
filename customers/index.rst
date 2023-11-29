.. CustomerService documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CustomerService's documentation!
===========================================

Customer Service API
====================

This module is a Flask application for a Customer Service API. It consists of functions for managing customer information and their wallet transactions.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Endpoints
---------

1. **Register Customer**

   - **URL:** `/register`
   - **Method:** `POST`
   - **Description:** Registers a new customer with the given details.
   - **Example Request:**

     .. code-block:: json

        {
          "username": "john_doe",
          "full_name": "John Doe",
          "password": "password123",
          "age": 30,
          "address": "123 Main St",
          "gender": "Male",
          "marital_status": "Single"
        }

   - **Example Response:**

     .. code-block:: json

        {"message": "Customer registered successfully"}

2. **Delete Customer**

   - **URL:** `/delete/<username>`
   - **Method:** `DELETE`
   - **Description:** Deletes the customer with the specified username.
   - **Example Response:**

     .. code-block:: json

        {"message": "Customer deleted successfully"}

3. **Update Customer**

   - **URL:** `/update/<username>`
   - **Method:** `PUT`
   - **Description:** Updates information for the customer with the specified username.
   - **Example Response:**

     .. code-block:: json

        {"message": "Customer updated successfully"}

4. **Get All Customers**

   - **URL:** `/customers`
   - **Method:** `GET`
   - **Description:** Retrieves a list of all customers.
   - **Example Response:**

     .. code-block:: json

        {
          "Customers": [
            {"username": "john_doe", "full_name": "John Doe", "age": 30, ...},
            ...
          ]
        }

5. **Get Customer**

   - **URL:** `/customer/<username>`
   - **Method:** `GET`
   - **Description:** Retrieves information for a specific customer.
   - **Example Response:**

     .. code-block:: json

        {
          "username": "john_doe",
          "full_name": "John Doe",
          "age": 30,
          ...
        }

6. **Charge Wallet**

   - **URL:** `/charge_wallet/<username>`
   - **Method:** `POST`
   - **Description:** Adds funds to the customer's wallet.
   - **Example Request:**

     .. code-block:: json

        {"amount": 100.0}

   - **Example Response:**

     .. code-block:: json

        {"message": "100.0 added to wallet", "new_balance": 150.0}

7. **Deduct Wallet**

   - **URL:** `/deduct_wallet/<username>`
   - **Method:** `POST`
   - **Description:** Deducts an amount from the customer's wallet.
   - **Example Request:**

     .. code-block:: json

        {"amount": 50.0}

   - **Example Response:**

     .. code-block:: json

        {"message": "50.0 deducted from wallet", "new_balance": 50.0}

8. **Get Wallet Balance**

   - **URL:** `/balance/<username>`
   - **Method:** `GET`
   - **Description:** Retrieves the balance of the customer's wallet.
   - **Example Response:**

     .. code-block:: json

        {"username": "john_doe", "balance": 100.0}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. automodule:: customers.app
    :members:
    :private-members:
