import socket

#HOST = "127.0.0.1"  # The server's hostname or IP address
HOST = "192.168.1.101"  # The server's hostname or IP address
PORT = 8765  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))
    #s.sendall(b"SEND")
    #data = s.recv(1024)
    s.sendall(b"END")
    s.close()

            
