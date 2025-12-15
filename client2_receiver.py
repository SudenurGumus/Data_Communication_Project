import socket

# -------- SAME FUNCTIONS AS CLIENT 1 --------
def parity_bit(data: str) -> str:
    bits = ''.join(format(ord(c), '08b') for c in data)
    return '0' if bits.count('1') % 2 == 0 else '1'


def parity_2d(data: str) -> str:
    matrix = [format(ord(c), '08b') for c in data]

    row_parity = ''
    for row in matrix:
        row_parity += '0' if row.count('1') % 2 == 0 else '1'

    col_parity = ''
    for i in range(8):
        col = ''.join(row[i] for row in matrix)
        col_parity += '0' if col.count('1') % 2 == 0 else '1'

    return row_parity + col_parity



def crc16(data: str) -> str:
    crc = 0xFFFF
    for char in data:
        crc ^= ord(char)
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return format(crc & 0xFFFF, '04X')


def internet_checksum(data: str) -> str:
    if len(data) % 2 != 0:
        data += '\0'

    checksum = 0
    for i in range(0, len(data), 2):
        word = (ord(data[i]) << 8) + ord(data[i+1])
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF
    return format(checksum, '04X')


# ---------------- MAIN ----------------
HOST = 'localhost'
PORT = 6000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Client 2 waiting...")

conn, addr = server.accept()
packet = conn.recv(2048).decode()
conn.close()

data, method, incoming_control = packet.split("|", 2)
data = data.rstrip('\x00').strip()

if method == "PARITY":
    computed = parity_bit(data)
elif method == "2D_PARITY":
    computed = parity_2d(data)
elif method == "CRC16":
    computed = crc16(data)
elif method == "CHECKSUM":
    computed = internet_checksum(data)
else:
    computed = "N/A"

status = "DATA CORRECT" if computed == incoming_control else "DATA CORRUPTED"

print("\nReceived Data :", data)
print("Method :", method)
print("Sent Check Bits :", incoming_control)
print("Computed Check Bits :", computed)
print("Status :", status)
