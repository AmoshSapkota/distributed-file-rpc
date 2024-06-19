import asyncio
import struct

class RPCClient:
    def __init__(self):
        self.client_reader = None
        self.client_writer = None
        self.results = {}

    async def connect(self, server_address):
        self.client_reader, self.client_writer = await asyncio.open_connection(*server_address)

    async def async_calculate_pi(self):
        rpc_name = 'async_calculate_pi'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        request_id = await self.client_reader.read(36)
        request_id = request_id.decode().strip()
        self.results[request_id] = None
        return request_id

    async def async_add(self, i, j):
        rpc_name = 'async_add'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        i_data = struct.pack('i', i)
        j_data = struct.pack('i', j)
        self.client_writer.write(i_data)
        self.client_writer.write(j_data)
        await self.client_writer.drain()
        request_id = await self.client_reader.read(36)
        request_id = request_id.decode().strip()
        self.results[request_id] = None
        return request_id

    async def async_sort(self, arrayA):
        rpc_name = 'async_sort'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        arrayA_length = struct.pack('i', len(arrayA))
        arrayA_data = struct.pack(f'{len(arrayA)}i', *arrayA)
        self.client_writer.write(arrayA_length)
        self.client_writer.write(arrayA_data)
        await self.client_writer.drain()
        request_id = await self.client_reader.read(36)
        request_id = request_id.decode().strip()
        self.results[request_id] = None
        return request_id

    async def async_matrix_multiply(self, matrixA, matrixB):
        rpc_name = 'async_matrix_multiply'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        matrixA_rows_cols = struct.pack('ii', len(matrixA), len(matrixA[0]))
        matrixA_data = struct.pack(f'{len(matrixA) * len(matrixA[0])}f', *matrixA.flatten())

        matrixB_rows_cols = struct.pack('ii', len(matrixB), len(matrixB[0]))
        matrixB_data = struct.pack(f'{len(matrixB) * len(matrixB[0])}f', *matrixB.flatten())

        self.client_writer.write(matrixA_rows_cols)
        self.client_writer.write(matrixA_data)
        self.client_writer.write(matrixB_rows_cols)
        self.client_writer.write(matrixB_data)
        await self.client_writer.drain()
        request_id = await self.client_reader.read(36)
        request_id = request_id.decode().strip()
        self.results[request_id] = None
        return request_id

    async def get_async_result(self, request_id):
        rpc_name = 'async_result'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        self.client_writer.write(request_id.encode())
        await self.client_writer.drain()
        response = await self.client_reader.read(1024)
        if response == b'PENDING':
            return None
        else:
            result = struct.unpack('f', response)[0]
            return result

    async def deferred_calculate_pi(self):
        rpc_name = 'deferred_calculate_pi'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        result = await self.client_reader.read(4)
        result = struct.unpack('f', result)[0]
        return result

    async def deferred_add(self, i, j):
        rpc_name = 'deferred_add'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        i_data = struct.pack('i', i)
        j_data = struct.pack('i', j)
        self.client_writer.write(i_data)
        self.client_writer.write(j_data)
        await self.client_writer.drain()
        result = await self.client_reader.read(4)
        result = struct.unpack('i', result)[0]
        return result

    async def deferred_sort(self, arrayA):
        rpc_name = 'deferred_sort'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        arrayA_length = struct.pack('i', len(arrayA))
        arrayA_data = struct.pack(f'{len(arrayA)}i', *arrayA)
        self.client_writer.write(arrayA_length)
        self.client_writer.write(arrayA_data)
        await self.client_writer.drain()
        result = await self.client_reader.read(len(arrayA) * 4)
        result = struct.unpack(f'{len(arrayA)}i', result)
        return result

    async def deferred_matrix_multiply(self, matrixA, matrixB):
        rpc_name = 'deferred_matrix_multiply'
        self.client_writer.write(rpc_name.encode())
        await self.client_writer.drain()
        matrixA_rows_cols = struct.pack('ii', len(matrixA), len(matrixA[0]))
        matrixA_data = struct.pack(f'{len(matrixA) * len(matrixA[0])}f', *matrixA.flatten())

        matrixB_rows_cols = struct.pack('ii', len(matrixB), len(matrixB[0]))
        matrixB_data = struct.pack(f'{len(matrixB) * len(matrixB[0])}f', *matrixB.flatten())

        self.client_writer.write(matrixA_rows_cols)
        self.client_writer.write(matrixA_data)
        self.client_writer.write(matrixB_rows_cols)
        self.client_writer.write(matrixB_data)
        await self.client_writer.drain()
        result = await self.client_reader.read(len(matrixA) * len(matrixB[0]) * 4)
        result = struct.unpack(f'{len(matrixA) * len(matrixB[0])}f', result)
        return result

    async def close(self):
        if self.client_writer:
            self.client_writer.close()
            await self.client_writer.wait_closed()

async def main():
    client = RPCClient()

    # Asynchronous RPCs
    await client.connect(('localhost', 8080))
    try:
        while True:
            operation = input("Choose an operation (calculate_pi, add, sort, matrix_multiply, quit): ")
            if operation == 'calculate_pi':
                request_id = await client.async_calculate_pi()
                print(f"Async calculate_pi request ID: {request_id}")

                while True:
                    result = await client.get_async_result(request_id)
                    if result is None:
                        print("Result is still pending...")
                        await asyncio.sleep(1)
                    else:
                        print(f"Async result for request ID {request_id}: {result}")
                        break

            elif operation == 'add':
                i = int(input("Enter first number: "))
                j = int(input("Enter second number: "))
                request_id = await client.async_add(i, j)
                print(f"Async add request ID: {request_id}")

                while True:
                    result = await client.get_async_result(request_id)
                    if result is None:
                        print("Result is still pending...")
                        await asyncio.sleep(1)
                    else:
                        print(f"Async result for request ID {request_id}: {result}")
                        break

            elif operation == 'sort':
                arrayA = list(map(int, input("Enter numbers separated by spaces: ").split()))
                request_id = await client.async_sort(arrayA)
                print(f"Async sort request ID: {request_id}")

                while True:
                    result = await client.get_async_result(request_id)
                    if result is None:
                        print("Result is still pending...")
                        await asyncio.sleep(1)
                    else:
                        print(f"Async result for request ID {request_id}: {result}")
                        break

            elif operation == 'matrix_multiply':
                matrixA = []
                matrixB = []
                print("Enter matrix A row by row (enter 'done' when finished):")
                while True:
                    row = input()
                    if row.lower() == 'done':
                        break
                    matrixA.append(list(map(float, row.split())))
                print("Enter matrix B row by row (enter 'done' when finished):")
                while True:
                    row = input()
                    if row.lower() == 'done':
                        break
                    matrixB.append(list(map(float, row.split())))
                request_id = await client.async_matrix_multiply(matrixA, matrixB)
                print(f"Async matrix_multiply request ID: {request_id}")

                while True:
                    result = await client.get_async_result(request_id)
                    if result is None:
                        print("Result is still pending...")
                        await asyncio.sleep(1)
                    else:
                        print(f"Async result for request ID {request_id}: {result}")
                        break

            elif operation == 'quit':
                break

            else:
                print("Invalid operation. Please try again.")

    finally:
        await client.close()

    # Deferred Synchronous RPCs
    await client.connect(('localhost', 8081))
    try:
        while True:
            operation = input("Choose an operation (calculate_pi, add, sort, matrix_multiply, quit): ")
            if operation == 'calculate_pi':
                print("Result for deferred_calculate_pi:", await client.deferred_calculate_pi())

            elif operation == 'add':
                i = int(input("Enter first number: "))
                j = int(input("Enter second number: "))
                print("Result for deferred_add:", await client.deferred_add(i, j))

            elif operation == 'sort':
                arrayA = list(map(int, input("Enter numbers separated by spaces: ").split()))
                print("Result for deferred_sort:", await client.deferred_sort(arrayA))

            elif operation == 'matrix_multiply':
                matrixA = []
                matrixB = []
                print("Enter matrix A row by row (enter 'done' when finished):")
                while True:
                    row = input()
                    if row.lower() == 'done':
                        break
                    matrixA.append(list(map(float, row.split())))
                print("Enter matrix B row by row (enter 'done' when finished):")
                while True:
                    row = input()
                    if row.lower() == 'done':
                        break
                    matrixB.append(list(map(float, row.split())))
                print("Result for deferred_matrix_multiply:", await client.deferred_matrix_multiply(matrixA, matrixB))

            elif operation == 'quit':
                break

            else:
                print("Invalid operation. Please try again.")

    finally:
        await client.close()

asyncio.run(main())
