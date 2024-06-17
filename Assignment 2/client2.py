import socket
import sys
from pathlib import Path

# Constants
HOST = '127.0.0.1'
PORT = 8080  
BUFFER_SIZE = 1024

# Splitting the commands given in the terminal on the client side
def split_commands():
    commands = {}
    try:
        commands["command"] = sys.argv[1].strip().lower()
    except IndexError:
        failure("Command was not given")

    try:
        commands["filename"] = sys.argv[2].strip()
    except IndexError:
        failure("Filename is not provided")

    if commands["command"] == "upload":
        pass
    elif commands["command"] == "download":
        pass
    elif commands["command"] == "rename":
        try:
            commands["new_filename"] = sys.argv[3].strip()
        except IndexError:
            failure("New filename not provided")
    elif commands["command"] == "delete":
        pass
    else:
        failure("Invalid command")

    return commands

# Upload the file to the server
def upload_file(sock_et, filename):
    file = Path(filename)
    if not file.is_file():
        failure("File is invalid")
    file_size = file.stat().st_size
    print(f"File size: {file_size} bytes")  # Debugging statement
    command = bytearray("{}\n{}\n".format("UPLOAD", file.name).encode())
    sock_et.sendall(command)
    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            print(f"Sending data: {data[:50]}...")  # Debugging statement
            sock_et.sendall(data)
    response = sock_et.recv(BUFFER_SIZE).decode()
    print(f"Server response: {response}")  # Debugging statement

# Download from server to the client
def download_file(sock_et, filename):
    msg = "{}\n{}".format("DOWNLOAD", filename)
    sock_et.send(msg.encode())
    data = sock_et.recv(BUFFER_SIZE)
    if data:
        Path("downloads_from_server/").mkdir(parents=True, exist_ok=True)
        Path("downloads_from_server/{}".format(filename)).write_bytes(data)
    else:
        failure("Download failed or file not found")

# Rename the old file in the server to the new name that is given by the client
def rename_file(sock_et, filename, new_filename):
    msg = "{}\n{}\n{}".format("RENAME", filename, new_filename)
    sock_et.send(msg.encode())

# Delete file in the server
def delete_file(sock_et, filename):
    msg = "{}\n{}".format("DELETE", filename)
    sock_et.send(msg.encode())

def failure(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

# Main code
if __name__ == "__main__":
    args = split_commands()
    sock_et = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_et.connect((HOST, PORT))
    if args["command"] == "upload":
        upload_file(sock_et, args["filename"])
    elif args["command"] == "download":
        download_file(sock_et, args["filename"])
    elif args["command"] == "rename":
        rename_file(sock_et, args["filename"], args["new_filename"])
    elif args["command"] == "delete":
        delete_file(sock_et, args["filename"])
    sock_et.close()
