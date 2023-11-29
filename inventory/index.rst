.. InventoryService documentation master file, created by
   sphinx-quickstart on Tue Nov 28 20:52:43 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to InventoryService's documentation!
============================================

Inventory Service API
=====================

This module is a Flask application for an Inventory Service API. It consists of functions for managing inventory items.

Endpoints
---------

1. **Fetch All Goods**

   - **URL:** `/inventory/goods`
   - **Method:** `GET`
   - **Description:** Retrieve a list of all inventory items.
   - **Example Response:**

     .. code-block:: json

        {
          "Inventory": [
            {"name": "Item1", "category": "Category1", "price": 10.0, "stock_count": 100},
            {"name": "Item2", "category": "Category2", "price": 15.0, "stock_count": 50}
          ]
        }

2. **Fetch a Specific Good**

   - **URL:** `/inventory/goods/{name}`
   - **Method:** `GET`
   - **Description:** Retrieve details for a specific inventory item.
   - **Example Response:**

     .. code-block:: json

        {"name": "Item1", "category": "Category1", "price": 10.0, "stock_count": 100}

3. **Add Goods**

   - **URL:** `/inventory/add`
   - **Method:** `POST`
   - **Description:** Add a new inventory item.
   - **Example Request:**

     .. code-block:: json

        {
          "name": "NewItem",
          "category": "NewCategory",
          "price": 20.0,
          "description": "Description of the new item",
          "stock_count": 50
        }

   - **Example Response:**

     .. code-block:: json

        {"message": "Item added successfully"}

4. **Update Goods**

   - **URL:** `/inventory/update/{item_id}`
   - **Method:** `PUT`
   - **Description:** Update details for a specific inventory item.
   - **Example Request:**

     .. code-block:: json

        {"price": 25.0, "stock_count": 75}

   - **Example Response:**

     .. code-block:: json

        {"message": "Item updated successfully"}

5. **Deduce Goods**

   - **URL:** `/inventory/deduce/{item_id}`
   - **Method:** `POST`
   - **Description:** Deduce stock from a specific inventory item.
   - **Example Request:**

     .. code-block:: json

        {"amount": 5}

   - **Example Response:**

     .. code-block:: json

        {"message": "5 units deduced", "new_stock_count": 70}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. automodule:: inventory.app
    :members:
    :private-members:
