import asyncio
import struct
import numpy as np

SERVER_ADDRESS = ('localhost', 8081)  # Different port from async server

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

async def handle_request(client_reader, client_writer):
    rpc_name = await client_reader.read(1024)
    rpc_name = rpc_name.decode().strip()

    if rpc_name == 'deferred_calculate_pi':
        asyncio.create_task(deferred_calculate_pi(client_writer))
    elif rpc_name == 'deferred_add':
        parameters = await client_reader.read(8)
        i, j = struct.unpack('ii', parameters)
        asyncio.create_task(deferred_add(client_writer, i, j))
    elif rpc_name == 'deferred_sort':
        arrayA_length_data = await client_reader.read(4)
        arrayA_length = struct.unpack('i', arrayA_length_data)[0]
        arrayA_data = await client_reader.read(arrayA_length * 4)
        arrayA = struct.unpack(f'{arrayA_length}i', arrayA_data)
        asyncio.create_task(deferred_sort(client_writer, arrayA))
    elif rpc_name == 'deferred_matrix_multiply':
        matrixA_rows_cols_data = await client_reader.read(8)
        matrixA_rows, matrixA_cols = struct.unpack('ii', matrixA_rows_cols_data)
        matrixA_length = matrixA_rows * matrixA_cols
        matrixA_data = await client_reader.read(matrixA_length * 4)
        matrixA = struct.unpack(f'{matrixA_length}f', matrixA_data)

        matrixB_rows_cols_data = await client_reader.read(8)
        matrixB_rows, matrixB_cols = struct.unpack('ii', matrixB_rows_cols_data)
        matrixB_length = matrixB_rows * matrixB_cols
        matrixB_data = await client_reader.read(matrixB_length * 4)
        matrixB = struct.unpack(f'{matrixB_length}f', matrixB_data)

        asyncio.create_task(deferred_matrix_multiply(client_writer, matrixA, matrixB))

    await client_writer.drain()

async def deferred_calculate_pi(client_writer):
    await asyncio.sleep(2)  # Simulate delay
    result = calculate_pi()
    client_writer.write(struct.pack('f', result))
    await client_writer.drain()
    client_writer.close()

async def deferred_add(client_writer, i, j):
    await asyncio.sleep(2)  # Simulate delay
    result = add(i, j)
    client_writer.write(struct.pack('i', result))
    await client_writer.drain()
    client_writer.close()

async def deferred_sort(client_writer, arrayA):
    await asyncio.sleep(2)  # Simulate delay
    result = sort(arrayA)
    client_writer.write(struct.pack(f'{len(result)}i', *result))
    await client_writer.drain()
    client_writer.close()

async def deferred_matrix_multiply(client_writer, matrixA, matrixB):
    await asyncio.sleep(2)  # Simulate delay
    result = matrix_multiply(matrixA, matrixB)
    client_writer.write(struct.pack(f'{len(result)}f', *result))
    await client_writer.drain()
    client_writer.close()

async def start_server():
    server = await asyncio.start_server(handle_request, *SERVER_ADDRESS)
    print("Deferred Synchronous Server is running and listening for connections.")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_server())
