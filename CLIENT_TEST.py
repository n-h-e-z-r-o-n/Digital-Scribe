import socket
import cv2
import numpy as np
user_ide = '123fv'

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  # replace with the server's IP address
    server_port = 800  # replace with the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))

    while True:

        client.send(str('Hello from Hezron').encode("utf-8")[:1024])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()
