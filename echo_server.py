import socket
import sys
import threading

clients_list = []

def usage():
	print("syntax : echo_server <port> [-b]")
	print("sample : echo_server 1234 -b")

def lis_cli(client_socket,addr,optionB):
	while True:
		data = client_socket.recv(2048).decode()
		if not data:
			break
		elif optionB == True:
			print(data)
			for client in clients_list:
				client.send(data.encode())
		else:
			print(data)
			client_socket.send(data.encode())
	clients_list.remove(client_socket)
	client_socket.close()

def start_server(server_socket,optionB):
	try:
		while True:
			print("[Listening for connection]")
			(client_socket,addr) = server_socket.accept()
			clients_list.append(client_socket)
			print("[",addr,"connected]")
			t = threading.Thread(target = lis_cli, args = (client_socket,addr,optionB))
			t.start()
	except KeyboardInterrupt:
		print("\n[Server Closed]")
		for client in clients_list:
			client.send("quit".encode())
			client.close()
		server_socket.close()
		sys.exit(1)

def main():
	optionB = False
	usage()
	
	if len(sys.argv) == 3 and sys.argv[2] == '-b':
		optionB = True
	elif len(sys.argv) != 2:
		print("[Syntax Error]")
		sys.exit(1)

	port = int(sys.argv[1])
	server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(('127.0.0.1',port))
	server_socket.listen(10)

	start_server(server_socket,optionB)

if __name__ == '__main__':
	main()
