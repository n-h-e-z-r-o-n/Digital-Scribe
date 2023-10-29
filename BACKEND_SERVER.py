import socket

def run_server():
    # create a socket object
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
    server_ip = "127.0.0.1"  # SERVER
    port = 800  # Server port listening
    tcp_socket.bind((server_ip, port))
    tcp_socket.listen(0)   # listen for incoming connections
    print(f"SERVER IS LISTENING ON: {server_ip} :{port}")



    while True:
        client_socket, client_address = tcp_socket.accept()  # accept incoming connections
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        frame_byte_length = client_socket.recv(1024).decode("utf-8", errors="ignore")
        print(frame_byte_length)

    server.close()


run_server()
