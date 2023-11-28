.. SalesService documentation master file, created by
   sphinx-quickstart on Tue Nov 28 20:00:34 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SalesService's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Sales Service API
=================

This module is a Flask application for a Sales Service API. Consists of functions for managing goods, sales transactions, and sales history.

Goods Model
-----------

.. autoclass:: Goods
    :members:

    Represents a list of the available goods in the database.

    **Attributes:**

    - `name` (str): The name of the good.
    - `price` (float): The price of the good.
    - `totalAmount` (int): The amount of the good available.

Sales Model
-----------

.. autoclass:: Sales
    :members:

    Represents a sales transaction.

    **Attributes:**

    - `username` (str): The username of the customer that purchased the good.
    - `price` (float): The price of the sold good.
    - `name` (str): The name of the sold good.
    - `time` (datetime): Timestamp of the time the good was sold.

App Routes
----------

.. automodule:: your_module_name
    :members:
    :undoc-members:
    :show-inheritance:

    .. automethod:: home

    .. automethod:: display_goods

    .. automethod:: get_goods_info

    .. automethod:: sale_transaction

    .. automethod:: get_sales_history
