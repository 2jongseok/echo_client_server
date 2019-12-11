import socket
import sys
import os
import threading

def usage():
		print("syntax : echo_client <host> <port>")
		print("sample : echo+client 127.0.0.1 1234")

def check_receive(client_socket):
	while True:
		try:
			data = client_socket.recv(2048)
			if not data:
				break
			elif data.decode() == "quit":
				break
			print("[received from server]")
			print(data.decode())
			print("Input Request : ")
		except:
			pass

	print("[Server closed]")
	client_socket.close()
	os._exit(1)

def start_client(client_socket ,addr):

	print("[",addr, " connected]")
	try:
		thr = threading.Thread(target = check_receive, args = (client_socket,))
		thr.daemon = True
		Thr.start()
		print("Input Request >> ")
		while True:
			data = input()
			client_socket.send(data.encode())
			if(data == "quit"):
				break
		
	except KeyboardInterrupt:
		pass

	finally:
		print("\n[", addr, " disconnected]")
		client_socket.close()
		sys.exit(0)

def main():
	usage()
	if len(sys.argv) != 3:
		print("[Syntax Error]")
		sys.exit(1)
		
	host = sys.argv[1]
	port = int(sys.argv[2])
	addr = (host,port)
	try:
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client_socket.connect(addr)
	except Exception as e:
		print("[Failed to connect]")
		print(e)
		sys.exit(1)

	start_client(client_socket, addr)

if __name__=='__main__':
	main()