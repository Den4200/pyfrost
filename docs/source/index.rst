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

.. code-block:: python
   :linenos:

   from frost import FrostClient
   from frost.client import Status
   from frost.client.events import EvenStatus


   def get_status(name):
      """
      A helper function to get the status of an event.
      """
      status = None
      while status is None:
         status = EventStatus.get_status(name)

      return status


   def register():
      """
      Register a new user on the connected server.
      """
      print('Registration')

      # We have this loop here to ensure that registration was successful.
      # If get_status('register') returned Status.DUPLICATE_USERNAME.value,
      # this means that there is already another registered user with that username.
      register_status = None
      while register_status in (Status.DUPLICATE_USERNAME.value, None):
         username = input('Username: ')
         password = input('Password: ')

         client.register(username, password)
         register_status = get_status('register')

      print('Regstration was successful.')


   def login():
      """
      Login with as a registered user on the connected server.
      """
      print('Login')

      # We have this loop here to ensure the login was successful.
      # If get_status('login') returned Status.INVALID_AUTH.value,
      # this means that either the username or password entered
      # was incorrect
      login_status = None
      while login_status in (Status.INVALID_AUTH.value, None):
         username = input('Username: ')
         password = input('Password: ')

         client.login(username, password)
         login_status = get_status('login')

      print('Login was successful.')


   with FrostClient() as client:
      register()
      login()

      client.get_joined_rooms()
      get_status('get_joined_rooms')

      client.create_room('Super Cool Room')
      get_status('create_room')

   # quick start guide not done yet!

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
