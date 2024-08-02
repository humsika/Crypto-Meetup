# Crypto-MeetUp

## Overview
Crypto-MeetUp is a highly secure, end-to-end encrypted chatting platform designed to ensure the confidentiality and integrity of remote communications. Developed using Python and cutting-edge cryptographic techniques, this platform integrates a custom implementation of the Double-Ratchet algorithm. This approach guarantees both secure and efficient message transmission, making it an ideal solution for users requiring private and safe communication channels.

## Key Features
- **End-to-End Encryption**: All messages are encrypted at the client side before being sent and are only decrypted by the intended recipient.
- **Double-Ratchet Algorithm**: Utilizes this advanced cryptographic protocol to manage session keys, ensuring that each message has its own unique encryption.
- **User Authentication**: Robust authentication mechanisms are in place to verify the identity of each user upon connection.
- **Secure Connection Setup**: Employs cryptographic techniques for establishing and maintaining secure connections between users.
- **Real-Time Messaging**: Allows for immediate message delivery and reception with minimal latency, suitable for dynamic and interactive communication.
- **User Verification via Email**: Integrates an email-based OTP system for enhanced security during the user authentication process.

## Technologies Used
This project leverages several advanced technologies and libraries:
- **Python**: The primary programming language used.
- **Cryptography Library**: For implementing cryptographic functions and secure key management.
- **Socket Programming**: For real-time data transmission between clients and servers.
- **SMTPlib**: For handling OTP-based user authentication through emails.

## Project Structure
- `code.py`: Implements the cryptographic backend, including key management and encryption/decryption routines.
- `client.py`: Manages the client-side interface, handling input, output, and communication with the server.
- `server.py`: Controls server-side operations, manages connections, authenticates users, and routes messages.
- `Mail`: A custom class for handling the sending of OTP emails to users for verification purposes.

## Setup and Installation
Ensure Python 3.x is installed on your machine. Then, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourgithubusername/crypto-meetup.git
