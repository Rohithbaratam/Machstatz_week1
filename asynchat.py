#The asynchat module builds on asyncore to make it easier to implement protocols based on passing messages back and forth between server and client. 
#The async_chat class is an asyncore.dispatcher subclass that receives data and looks for a message terminator. 
#Your subclass only needs to specify what to do when data comes in and how to respond once the terminator is found. 
#Outgoing data is queued for transmission via FIFO objects managed by async_chat.

import asyncore
import logging
import socket

from asynchat_echo_handler import EchoHandler

class EchoServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """
    
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.listen(1)
        return

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        EchoHandler(sock=client_info[0])
        # We only want to deal with one client at a time,
        # so close as soon as we set up the handler.
        # Normally you would not do this and the server
        # would run forever or until it received instructions
        # to stop.
        self.handle_close()
        return
    
    def handle_close(self):
        self.close()
