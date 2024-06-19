import asyncio
import struct
import numpy as np
import uuid

SERVER_ADDRESS = ('localhost', 8080)
results = {}

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

    if rpc_name == 'async_calculate_pi':
        request_id = str(uuid.uuid4())
        asyncio.create_task(async_calculate_pi(request_id))
        client_writer.write(request_id.encode())
    elif rpc_name == 'async_add':
        request_id = str(uuid.uuid4())
        parameters = await client_reader.read(8)
        i, j = struct.unpack('ii', parameters)
        asyncio.create_task(async_add(request_id, i, j))
        client_writer.write(request_id.encode())
    elif rpc_name == 'async_sort':
        request_id = str(uuid.uuid4())
        arrayA_length_data = await client_reader.read(4)
        arrayA_length = struct.unpack('i', arrayA_length_data)[0]
        arrayA_data = await client_reader.read(arrayA_length * 4)
        arrayA = struct.unpack(f'{arrayA_length}i', arrayA_data)
        asyncio.create_task(async_sort(request_id, arrayA))
        client_writer.write(request_id.encode())
    elif rpc_name == 'async_matrix_multiply':
        request_id = str(uuid.uuid4())
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

        asyncio.create_task(async_matrix_multiply(request_id, matrixA, matrixB))
        client_writer.write(request_id.encode())
    elif rpc_name == 'async_result':
        request_id = await client_reader.read(36)
        request_id = request_id.decode().strip()
        if request_id in results:
            result = results.pop(request_id)
            client_writer.write(struct.pack('f', result))
        else:
            client_writer.write(b'PENDING')

    await client_writer.drain()
    client_writer.close()

async def async_calculate_pi(request_id):
    await asyncio.sleep(2)  # Simulate delay
    result = calculate_pi()
    results[request_id] = result

async def async_add(request_id, i, j):
    await asyncio.sleep(2)  # Simulate delay
    result = add(i, j)
    results[request_id] = result

async def async_sort(request_id, arrayA):
    await asyncio.sleep(2)  # Simulate delay
    result = sort(arrayA)
    results[request_id] = result

async def async_matrix_multiply(request_id, matrixA, matrixB):
    await asyncio.sleep(2)  # Simulate delay
    result = matrix_multiply(matrixA, matrixB)
    results[request_id] = result

async def start_server():
    server = await asyncio.start_server(handle_request, *SERVER_ADDRESS)
    print("Asynchronous Server is running and listening for connections.")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_server())
