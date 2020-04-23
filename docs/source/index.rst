Welcome to the PyFrost documentation!
=====================================

.. image:: https://i.imgur.com/mbhyPMh.jpg

Quick Start
-----------
Using PyFrost, it's quite simple to quickly fire up a server with clients.

Here's a simple server.

.. code-block:: python
   :linenos:

   from frost import FrostServer


   server = FrostServer(__file__)
   server.run(ip='127.0.0.1', port=5555)


Here's a simple client.

.. literalinclude:: ../../tests/example_client.py
   :language: python
   :linenos:


The Official Client
-------------------
The official client for this library is under development.
You can test it out and/or contribute to the `repository <https://www.github.com/Den4200/apollo/>`_.

The Source Code
---------------
The source is available `here <https://www.github.com/Den4200/pyfrost/>`_ on GitHub.
Feel free to contribute to this project.

Contents
--------
.. toctree::
   :maxdepth: 4
   :glob:

   frost
