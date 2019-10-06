'''
	Simple udp socket server
'''

import socket
import sys

HOST = ''	# Symbolic name meaning all available interfaces
PORT = 8888	# Arbitrary non-privileged port

active_peers = {}

def _send_message(message, sock, host, port):
    try :
        sock.sendto(str(message).encode("utf-8"), (host, port))
        
    except socket.error as msg:
        print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()


def main():

	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print('Socket created')
	except socket.error as msg :
		print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
		sys.exit()


	# Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error as msg:
		print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
		sys.exit()
		
	print('Socket bind complete')

	#now keep talking with the client
	while 1:
		# receive data from client (data, addr)
		d = s.recvfrom(1024)
		data = str(d[0], "utf-8")
		addr = d[1]
		
		if str(data).startswith("REGISTER"):
			active_peers[data.split()[1]] = addr

		if str(data) == "LIST":
			print("LIST")
			print(active_peers)
			msg = "LIST {}".format(active_peers)

			_send_message(message=msg, sock=s, host=addr[0], port=addr[1])
		
		print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip())
		
	s.close()


if __name__ == "__main__":
	main()
