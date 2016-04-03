#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '127.0.0.1' # Get local machine name
port = 6000                # Reserve a port for your service.

s.connect((host, port))
s.send('1024')
s.close                     # Close the socket when done