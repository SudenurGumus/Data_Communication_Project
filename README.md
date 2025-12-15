# Data-Transmission-with-Error-Detection-Methods

## Project Overview

This project demonstrates data transmission with error detection techniques using socket programming.
The system simulates a real network environment by introducing random transmission errors and
verifying data integrity at the receiver side.

The system includes:

- Random error detection method selection
- Random error injection during transmission
- Correct handling of corrupted and non-corrupted data

The project consists of three main components:

1. Client 1 (Sender)
2. Server (Intermediate Node + Error Injector)
3. Client 2 (Receiver + Error Controller)

---

## System Architecture
- Client 1 generates control bits and sends the packet.
- The server may corrupt the transmitted data.
- Client 2 verifies data integrity using the selected method.

---

## Packet Format

All transmitted packets follow the same structure:
Example:
---

## Implemented Error Detection Methods

- Parity Bit (Even Parity)
- 2D Parity (Row and Column Parity)
- CRC-16
- Internet Checksum
- Hamming (7,4) Encoding

---

## Proxy Server – Error Injection

The server simulates an unreliable communication channel by corrupting transmitted data with a
probability of 50%. Only the data part of the packet is modified, while control bits remain unchanged.

Possible error types:

- Bit flip
- Character substitution
- Character deletion
- Character insertion
- Character swapping

---

## Execution Flow

1. Client 1 reads user input and generates control bits.
2. The packet is sent to the server.
3. The server may corrupt the data.
4. The packet is forwarded to Client 2.
5. Client 2 recomputes control bits and verifies data integrity.

---

## Project Structure
---

## Notes

- This project is intended for educational purposes.
- Only one connection is handled per execution.
- Hamming code is used for encoding only; decoding and correction are not implemented.
- The | character should not be used inside message content.

---

## Technologies Used

- Python 3
- TCP Socket Programming
- Randomized Error Simulation
