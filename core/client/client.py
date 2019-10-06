'''
	UDP socket client
'''
import threading
import time
import socket
import sys
import random


mediator_host = 'manuelpm.com';
mediator_port = 8888;

CLIENT_BASE_UDP_PORT = 55000

class ClientThread(threading.Thread):
   def __init__(self, threadID, name, sock, function, config):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.sock = sock
      self.function = function
      self.config = config
   def run(self):
      print("Starting " + self.name)
      self.function(self.sock, self.config)
      print("Exiting " + self.name)


def receive_messages(sock, config):
    while(True):
        try:
            message, addr = sock.recvfrom(1024)
            message = str(message, "utf-8")
            print("{}: {}".format(addr, message))
            if message.startswith("LIST"):
                active_peers = eval(message[5:])
                print("Active peers:")
                print(active_peers)
                for peer, addr in active_peers.items():
                    if peer != config["client_id"]:
                        find_peer_port(sock, peer, addr, config)


        except socket.error as msg:
            print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

def read_input_and_send(sock, config):
    while(True):
        msg = input("[{}]> ".format(config["client_id"]))
        _send_message(message=msg, sock=sock, host=mediator_host, port=mediator_port)


def heartbeat_to_mediator(sock, config):
    while(True):
        msg = "REGISTER {}".format(config["client_id"])
        _send_message(message=msg, sock=sock, host=mediator_host, port=mediator_port)
        msg = "LIST"
        _send_message(message=msg, sock=sock, host=mediator_host, port=mediator_port)
        time.sleep(10)

def find_peer_port(sock, peer_id, peer_addr, config):
    for i in range(2):
        #for p in range(1, 65535):
        msg = "SNIFFING from {} for {}".format(config["client_id"], peer_id)
        print("")
        _send_message(message=msg, sock=config["sock_client"], host=peer_addr[0], port=peer_addr[1]+10)

def _send_message(message, sock, host, port):
    try :
        sock.sendto(str(message).encode("utf-8"), (host, port))
        
    except socket.error as msg:
        print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

def main():
    
    active_peers = {}
    config = {}
    client_id = input("How do you wanna register?\n")
    print("Starting client: [{}]".format(client_id))

    local_port = random.randint(20000, 29989)

    config["client_id"] = client_id
    config["client_port"] = local_port

    try:
        sock_mediator = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    try:
        sock_mediator.bind(('', config["client_port"]))
        sock_client.bind(('', config["client_port"] + 10))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    config["sock_mediator"] = sock_mediator
    config["sock_client"] = sock_client

    listener_thread = ClientThread(1, "listener", sock_mediator, receive_messages, config)
    sender_thread = ClientThread(2, "manuelpm87", sock_mediator, read_input_and_send, config)
    heartbeat_thread = ClientThread(3, "heartbeat", sock_mediator, heartbeat_to_mediator, config)

    listener_thread.start()
    sender_thread.start()
    heartbeat_thread.start()

    listener_thread.join()
    sender_thread.join()
    heartbeat_thread.join()


if __name__ == "__main__":
    main()
