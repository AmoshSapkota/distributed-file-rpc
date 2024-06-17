import socket
import struct
import numpy as np

SERVER_ADDRESS = ('localhost', 8080)

def calculate_pi():
    return 3.14159

def add(i, j):
    return i + j

def sort(arrayA):
    return sorted(arrayA)

def matrix_multiply(matrixA, matrixB):
    matrixA = np.array(matrixA).reshape(-1, len(matrixB) // len(matrixA))
    matrixB = np.array(matrixB).reshape(len(matrixA[0]), -1)
    matrixC = np.dot(matrixA, matrixB)
    return matrixC.flatten().tolist()

def handle_request(client_socket):
    rpc_name = client_socket.recv(1024).decode()

    if rpc_name == 'calculate_pi':
        result = calculate_pi()
        client_socket.sendall(struct.pack('f', result))
    elif rpc_name == 'add':
        i, j = struct.unpack('ii', client_socket.recv(8))
        result = add(i, j)
        client_socket.sendall(struct.pack('i', result))
    elif rpc_name == 'sort':
        arrayA_length = struct.unpack('i', client_socket.recv(4))[0]
        arrayA = struct.unpack(f'{arrayA_length}i', client_socket.recv(arrayA_length * 4))
        result = sort(arrayA)
        client_socket.sendall(struct.pack(f'{len(result)}i', *result))
    elif rpc_name == 'matrix_multiply':
        matrixA_length = struct.unpack('i', client_socket.recv(4))[0]
        matrixA = struct.unpack(f'{matrixA_length}f', client_socket.recv(matrixA_length * 4))
        
        matrixB_length = struct.unpack('i', client_socket.recv(4))[0]
        matrixB = struct.unpack(f'{matrixB_length}f', client_socket.recv(matrixB_length * 4))

        result = matrix_multiply(matrixA, matrixB)
        client_socket.sendall(struct.pack(f'{len(result)}f', *result))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)
    
    print("Server is running and listening for connections.")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")
        handle_request(client_socket)
        client_socket.close()

if __name__ == "__main__":
    start_server()
