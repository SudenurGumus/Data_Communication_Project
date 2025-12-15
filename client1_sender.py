import socket

# ---------------- PARITY ----------------
def parity_bit(data: str) -> str:
    bits = ''.join(format(ord(c), '08b') for c in data)
    return '0' if bits.count('1') % 2 == 0 else '1'


# ---------------- 2D PARITY ----------------
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



# ---------------- CRC16 ----------------
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


# ---------------- HAMMING (7,4) ----------------
def hamming_encode(data: str) -> str:
    encoded = ""
    for char in data:
        b = format(ord(char), '08b')
        for i in range(0, 8, 4):
            d = list(map(int, b[i:i+4]))
            p1 = d[0] ^ d[1] ^ d[3]
            p2 = d[0] ^ d[2] ^ d[3]
            p3 = d[1] ^ d[2] ^ d[3]
            encoded += f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}"
    return encoded


# ---------------- INTERNET CHECKSUM ----------------
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
PORT = 5000

print("Enter message:")
message = input()
message = message.strip()

print("\nChoose Method:")
print("1 - Parity")
print("2 - 2D Parity")
print("3 - CRC16")
print("4 - Hamming Code")
print("5 - Internet Checksum")

choice = input("Choice: ")

if choice == "1":
    method = "PARITY"
    control = parity_bit(message)
elif choice == "2":
    method = "2D_PARITY"
    control = parity_2d(message)
elif choice == "3":
    method = "CRC16"
    control = crc16(message)
elif choice == "4":
    method = "HAMMING"
    control = hamming_encode(message)
elif choice == "5":
    method = "CHECKSUM"
    control = internet_checksum(message)
else:
    print("Invalid choice")
    exit()

packet = f"{message}|{method}|{control}"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(packet.encode())
client.close()

print("\nPacket Sent:")
print(packet)
