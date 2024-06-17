import socket
import os

# Constants
HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024
BASE_DIR = 'server_files'

# Ensure the base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

def handle_client(conn):
    with conn:
        data = conn.recv(BUFFER_SIZE).decode().split()
        command = data[0]

        if command == 'UPLOAD':
            filename = data[1]
            handle_upload(conn, filename)
        elif command == 'DOWNLOAD':
            filename = data[1]
            handle_download(conn, filename)
        elif command == 'DELETE':
            filename = data[1]
            handle_delete(conn, filename)
        elif command == 'RENAME':
            old_filename, new_filename = data[1], data[2]
            handle_rename(conn, old_filename, new_filename)
        else:
            conn.sendall(b'INVALID COMMAND')

def handle_upload(conn, filename):
    file_path = os.path.join(BASE_DIR, filename)
    with open(file_path, 'wb') as f:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)
    conn.sendall(b'UPLOAD SUCCESS')

def handle_download(conn, filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        conn.sendall(b'DOWNLOAD READY')
        with open(file_path, 'rb') as f:
            conn.sendfile(f)
    else:
        conn.sendall(b'FILE NOT FOUND')

def handle_delete(conn, filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        conn.sendall(b'DELETE SUCCESS')
    else:
        conn.sendall(b'FILE NOT FOUND')

def handle_rename(conn, old_filename, new_filename):
    old_file_path = os.path.join(BASE_DIR, old_filename)
    new_file_path = os.path.join(BASE_DIR, new_filename)
    if os.path.exists(old_file_path):
        os.rename(old_file_path, new_file_path)
        conn.sendall(b'RENAME SUCCESS')
    else:
        conn.sendall(b'FILE NOT FOUND')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')
        
        while True:
            conn, addr = s.accept()
            print(f'Connected by {addr}')
            handle_client(conn)

if __name__ == '__main__':
    main()
