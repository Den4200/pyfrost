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
   from frost.client.events import EventStatus
   from frost.client.objects import Memory


   def get_status(name):
      """
      A helper function to get the status of an event.
      """
      status = None
      while status is None:
         status = EventStatus.get_status(name)

      return Status(status)


   def register():
      """
      Register a new user on the connected server.
      """
      print('Registration')

      # We have this loop here to ensure that registration was successful.
      # If get_status('register') returned Status.DUPLICATE_USERNAME,
      # this means that there is already another registered user with that username.
      register_status = None
      while register_status != Status.SUCCESS:
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
      # If get_status('login') returned Status.INVALID_AUTH,
      # this means that either the username or password entered
      # was incorrect
      login_status = None
      while login_status != Status.SUCCESS:
         username = input('Username: ')
         password = input('Password: ')

         client.login(username, password)
         login_status = get_status('login')

      print('Login was successful.')


   with FrostClient() as client:
      register()
      login()

      room_name = 'Super Cool Room'

      # Create a new room in the server
      client.create_room(room_name)
      create_room_status = get_status('create_room')

      if create_room_status == Status.SUCCESS:
         print('Room successfully created!')
      else:
         raise Exception(f'Error: {create_room_status}')

      # Get the rooms we've joined (The room we just created)
      client.get_joined_rooms()
      get_status('get_joined_rooms')

      # Get the ID of the room we just created
      for room_id, room in Memory.rooms:
         if room.name == room_name:
            cool_room_id = room_id
            break

      # Send a message to your new room!
      client.send_msg(cool_room_id, 'This is the new room I've just created!')

      # Get the invite code to your room, so your friends can join
      client.get_invite_code(cool_room_id)
      invite_code_status = Status(get_status('get_invite_code'))

      if invite_code_status == Status.SUCCESS:
         invite_code = Memory.rooms[cool_room_id].invite_code
         print(f'Invite code: {invite_code}')
      else:
         raise Exception(f'Error: {invite_code_status}')

      # To join your friend's room, ask them for the invite code
      # Example invite code below - not real
      invite_code = 'aff10152-6d4c-11ea-87fe-9cb6d0d6fdc2'

      client.join_room(invite_code)
      join_room_status = get_status('join_room')

      if join_room_status == Status.SUCCESS:
         print('Successfully joined ')

      # now, get the room and send a msg

   # not done yet!

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
