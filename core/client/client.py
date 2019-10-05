'''
	UDP socket client
'''
import threading
import time
import socket
import sys


mediator_host = '127.0.0.1';
mediator_port = 8888;

client_id = sys.argv[1]

class ClientThread(threading.Thread):
   def __init__(self, threadID, name, sock, function):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.sock = sock
      self.function = function
   def run(self):
      print("Starting " + self.name)
      self.function(self.sock)
      print("Exiting " + self.name)


def receive_messages(sock):
    while(True):
        try:
            message, addr = sock.recvfrom(1024)
            print("{}: {}".format(addr, str(message, "utf-8")))

        except socket.error as msg:
            print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

def read_input_and_send(sock):
    while(True):
        msg = input("[{}]> ".format(client_id))
        _send_message(message=msg, sock=sock, host=mediator_host, port=mediator_port)


def heartbeat_to_mediator(sock):
    while(True):
        msg = "REGISTER {}".format(client_id)
        _send_message(message=msg, sock=sock, host=mediator_host, port=mediator_port)
        time.sleep(10)


def _send_message(message, sock, host, port):
    try :
        sock.sendto(str(message).encode("utf-8"), (host, port))
        
    except socket.error as msg:
        print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

def main():

    print("Starting client: [{}]".format(client_id))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()


    listener_thread = ClientThread(1, "listener", s, receive_messages)
    sender_thread = ClientThread(2, "manuelpm87", s, read_input_and_send)
    heartbeat_thread = ClientThread(3, "heartbeat", s, heartbeat_to_mediator)

    listener_thread.start()
    sender_thread.start()
    heartbeat_thread.start()

    listener_thread.join()
    sender_thread.join()
    heartbeat_thread.join()


if __name__ == "__main__":
    main()
