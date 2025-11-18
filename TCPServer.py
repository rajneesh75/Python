import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to host and port
server_socket.bind(('localhost', 9999))

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening...")

# Accept a connection
client_socket, addr = server_socket.accept()
print("Connection from:", addr)

# Send and receive data
data = client_socket.recv(1024)
print("Received:", data.decode())
client_socket.send(b"Hello from server!")


# Close connections
client_socket.close()
server_socket.close()
