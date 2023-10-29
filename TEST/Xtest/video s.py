import socket
import cv2
import numpy as np
import ast


def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    print(server_ip)
    #server_ip = "41.90.187.99"
    port = 800

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip} :{port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # receive data from the client
    count = 1
    hold: int = 0
    hold2: tuple = (0, 0, 0)
    while True:

        frame_byte_length = client_socket.recv(1024).decode("utf-8", errors="ignore")
        try:
            frame_byte_length = int(frame_byte_length)
        except:
            frame_byte_length = hold

        frame_shape = client_socket.recv(1024)
        try:
            frame_shape = frame_shape.decode("utf-8")
            frame_shape = ast.literal_eval(frame_shape)
        except:
            frame_shape = hold2

        frame_array_in_byte = client_socket.recv(frame_byte_length)
        try:
            frame_array = np.frombuffer(frame_array_in_byte, dtype=np.uint8).reshape(frame_shape[0], frame_shape[1], frame_shape[2])
            cv2.imshow('Video Chat', frame_array)
        except:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count +=1
        hold =  frame_byte_length
        hold2 = frame_shape
    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()


run_server()
