import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

# Send response
client_socket.send(b"Hello Server!")

# Receive message from server
print(client_socket.recv(1024).decode())

client_socket.close()
