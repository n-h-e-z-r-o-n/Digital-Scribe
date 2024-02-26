import socket


def client_program():
    domain = "inspiring-frost-18221.pktriot.net"
    ip = socket.gethostbyname(domain)
    port = 22575  # socket server port number
    host = ip


    host = "127.0.0.1"  # as both code is running on same pc
    port = 800  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    login_credentials = 'login_Request~m@gmail~12maureen12'
    client_socket.send(login_credentials.encode("utf-8")[:1024])  # send message

    data = client_socket.recv(1024).decode("utf-8", errors="ignore")  # receive response

    print('Received from server: ' + data)  # show in terminal



    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()