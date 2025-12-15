import socket
import random

HOST = 'localhost'
PORT = 5000
FORWARD_PORT = 6000

def corrupt_data(data: str) -> str:
    # %50 ihtimalle veri bozulmaz
    if random.random() < 0.5:
        return data

    if len(data) == 0:
        return data

    method = random.choice(["flip", "sub", "del", "ins", "swap"])
    data = list(data)

    if method == "flip":
        i = random.randint(0, len(data)-1)
        data[i] = chr(ord(data[i]) ^ 1)

    elif method == "sub":
        i = random.randint(0, len(data)-1)
        data[i] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    elif method == "del" and len(data) > 1:
        del data[random.randint(0, len(data)-1)]

    elif method == "ins":
        data.insert(random.randint(0, len(data)), random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    elif method == "swap" and len(data) > 1:
        i = random.randint(0, len(data)-2)
        data[i], data[i+1] = data[i+1], data[i]

    return ''.join(data)



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server listening...")

conn, addr = server.accept()
packet = conn.recv(1024).decode()
conn.close()

data, method, control = packet.split("|")

corrupted_data = corrupt_data(data)
new_packet = f"{corrupted_data}|{method}|{control}"

forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
forward.connect((HOST, FORWARD_PORT))
forward.send(new_packet.encode())
forward.close()

print("Original Data :", data)
print("Corrupted Data:", corrupted_data)
