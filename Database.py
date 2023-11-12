import socket
import time

server_IP4v_address = "192.168.100.9"  # "127.0.0.1"  # as both code is running on same pc
Server_listening_port = 800  # socket server port number
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
client_socket.connect((server_IP4v_address, Server_listening_port))
user_data = f"123~Hezron Maureen~phtptptpr"

client_socket.send(f"active~{len(user_data)}".encode("utf-8"))
client_socket.send(user_data.encode("utf-8"))




def fetch_info():
    list_hold = []  # clear the list
    global client_socket, user_id
    print("fetching")

    client_socket.send('infoRequest'.encode("utf-8")[:1024])  # send message
    while True:
        print("starting")
        buffer_size = client_socket.recv(500).decode("utf-8")
        info = client_socket.recv(int(buffer_size)).decode("utf-8")
        print("info")
        if info == "end":
            break
        info = info.split("~")

        print(info)
        #if int(info[0]) == int(user_id):
        #    continue

        list_hold.append((info[0], info[1], info[2]))
        break

    print("finished fetching")

    return list_hold

m = fetch_info()
print(m)

client_socket.close()
