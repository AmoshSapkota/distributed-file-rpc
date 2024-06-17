import socket
import struct

SERVER_ADDRESS = ('localhost', 8080)

def calculate_pi():
    rpc_name = 'calculate_pi'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    client_socket.sendall(rpc_name.encode())
    result = struct.unpack('f', client_socket.recv(4))[0]
    client_socket.close()
    return result

def add():
    rpc_name = 'add'
    i = int(input("Enter the first number: "))
    j = int(input("Enter the second number: "))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    client_socket.sendall(rpc_name.encode())
    client_socket.sendall(struct.pack('ii', i, j))
    result = struct.unpack('i', client_socket.recv(4))[0]
    client_socket.close()
    return result

def sort():
    rpc_name = 'sort'
    arrayA = list(map(int, input("Enter the numbers to sort (space-separated): ").split()))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    client_socket.sendall(rpc_name.encode())
    client_socket.sendall(struct.pack('i', len(arrayA)))
    client_socket.sendall(struct.pack(f'{len(arrayA)}i', *arrayA))
    result = struct.unpack(f'{len(arrayA)}i', client_socket.recv(len(arrayA) * 4))
    client_socket.close()
    return result

def matrix_multiply():
    rpc_name = 'matrix_multiply'
    matrixA = list(map(float, input("Enter the first matrix (flattened, space-separated): ").split()))
    matrixB = list(map(float, input("Enter the second matrix (flattened, space-separated): ").split()))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    client_socket.sendall(rpc_name.encode())
    client_socket.sendall(struct.pack('i', len(matrixA)))
    client_socket.sendall(struct.pack(f'{len(matrixA)}f', *matrixA))
    client_socket.sendall(struct.pack('i', len(matrixB)))
    client_socket.sendall(struct.pack(f'{len(matrixB)}f', *matrixB))
    result_length = len(matrixA) // (len(matrixB) // len(matrixA))
    result = struct.unpack(f'{result_length}f', client_socket.recv(result_length * 4))
    client_socket.close()
    return result

def main():
    while True:
        print("Select an operation:")
        print("1. Calculate Pi")
        print("2. Add")
        print("3. Sort")
        print("4. Matrix Multiply")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            print("Result:", calculate_pi())
        elif choice == '2':
            print("Result:", add())
        elif choice == '3':
            print("Result:", sort())
        elif choice == '4':
            print("Result:", matrix_multiply())
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
