#! /usr/bin/env python
#coding=utf-8
  
from tornado.tcpserver import TCPServer  
from tornado.ioloop  import IOLoop  
  
class Connection(object):  
    clients = set()  
    def __init__(self, stream, address): 
        Connection.clients.add(self) 
        self._stream = stream  
        self._address = address  
        self._stream.set_close_callback(self.on_close)  
        self.read_message()  
        print "New incoming connection", address 
      
    def read_message(self):  
        self._stream.read_until('\n', self.broadcast_messages)  
  
    def broadcast_messages(self, data):  
        print "User said:", data[:-1], self._address
        for conn in Connection.clients:  
            conn.send_message(data)  
        self.read_message()  
      
    def send_message(self, data):  
        self._stream.write(data) 
          
    def on_close(self):  
        print "Disconnect", self._address
        Connection.clients.remove(self)  
  
class Server(TCPServer):
    def handle_stream(self, stream, address): 
        """
        对每个传入连接都对应一个stream和一个address，在handle_stream中指定Handler (这难道不会导致同步问题 ？）
        """
        print "New connection :", address, stream 
        Connection(stream, address) 
        print "connection num is:", len(Connection.clients)
  
if __name__ == '__main__':  
    print "Server start ......"  
    server = Server()  
    server.listen(8889)  
    IOLoop.instance().start() 

