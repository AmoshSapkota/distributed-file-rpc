
## Project Overview
This project involves implementing a simple file upload and download service and a computation service using both message-oriented and remote procedure call (RPC) based communication. The project is divided into four assignments:

1. Single-threaded file server.
2. Multi-threaded file server.
3. Synchronous RPC-based computation server.
4. Asynchronous and deferred synchronous RPC-based computation server.


## Prerequisites
- Linux operating system (Ubuntu recommended)
- Python, Java or any other programming language
- Any other necessary development tools and libraries

## Setup Instructions

### Virtual Machine Setup (Assignment-0)
1. Install a virtual machine software (e.g., VirtualBox, VMware).
2. Download and install a Linux distribution (Ubuntu recommended) on the VM.
3. Test the Linux environment to ensure it is ready for development.

### Assignment-1: Single-threaded File Server
1. Create a directory structure to hold server and client files.
2. Implement the server to support UPLOAD, DOWNLOAD, DELETE, and RENAME operations using sockets.
3. Create client programs to test these operations.
4. Ensure the server listens on port 8080.

### Assignment-2: Multi-threaded File Server
1. Modify the single-threaded server to handle multiple client connections using threads.
2. Ensure each client connection is handled independently.
3. Test with multiple clients to ensure the server supports concurrent operations.

### Assignment-3: Synchronous RPC-based Computation Server
1. Implement the following RPCs:
   - `calculate_pi()`
   - `add(i, j)`
   - `sort(arrayA)`
   - `matrix_multiply(matrixA, matrixB, matrixC)`
2. Create client and server stubs to pack and unpack RPC parameters.
3. Implement the RPCs without using Java RMI or built-in RPC libraries in other languages.
4. Ensure the server correctly performs the computations and the client receives the results.

### Assignment-4: Asynchronous and Deferred Synchronous RPC-based Computation Server
1. Implement asynchronous RPCs where the server immediately acknowledges the RPC call and performs the computation later. The client can query the server for the result at a later time.
2. Implement deferred synchronous RPCs with a mechanism to interrupt the client when the server completes the computation and returns the result.
3. Modify the client design to handle asynchronous and deferred synchronous RPCs.

## Compilation and Execution

1. Navigate to the respective Assignment directory.
2. Compile the server and client programs.
