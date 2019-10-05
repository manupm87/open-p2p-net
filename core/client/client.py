'''
	UDP socket client
'''
import threading
import time
import socket
import sys


host = 'localhost';
port = 8888;

class ListenerThread(threading.Thread):
   def __init__(self, threadID, name, sock):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.sock = sock
   def run(self):
      print ("Starting " + self.name)
      receive_messages(self.sock)
      print ("Exiting " + self.name)

class WriterThread(threading.Thread):
   def __init__(self, threadID, name, sock):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.sock = sock
   def run(self):
      print ("Starting " + self.name)
      send_message(self.name, self.sock)
      print ("Exiting " + self.name)

def receive_messages(sock):
    while(True):
        try:
            message, addr = sock.recvfrom(1024)
            print("{}: {}".format(addr, message))

        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

def send_message(username, sock):
    while(1) :
        msg = raw_input("[{}]> ".format(username))
        
        try :
            #Set the whole string
            sock.sendto(msg, (host, port))
        
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()


def main():
    # create dgram udp socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    try:
        listener_thread = ListenerThread(1, "listener", s)
        sender_thread = WriterThread(2, "manuelpm87", s)

        listener_thread.start()
        sender_thread.start()

        listener_thread.join()
        sender_thread.join()
    
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    sys.exit(0)

if __name__ == "__main__":
    main()
