import socket
import hashlib
import select
import json

# ---------------------- creating a connection to the database.---------------------------------------------------------
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12hezron12",
    database="medscribe"
)
cursor = mydb.cursor()

active_connections = {}

# ========================================================== FUNCTIONS DEFINITIONS
# ========================================================== function to encrypt userdata.


def encryp(string):
    salt = "5gzbella"
    string = string + salt  # Adding salt to the password
    hashed = hashlib.md5(string.encode())  # Encoding the password
    return hashed.hexdigest()  # return the Hash


# ---------------------- function to validate login credentials. ------------------------


def Login_function(Email, password):
    cursor.execute("select * from users where Email=%s and Password=%s", (Email, password))
    query_result = cursor.fetchall()
    if len(query_result) == 0:
        return 'User_Error'
    else:
        return query_result[0][0]
def fetch_user_detal(user_id):
    cursor.execute("SELECT * FROM medscribe.users where user_id = %s;", [user_id])
    query_result = cursor.fetchall()
    return query_result[0]






# -----------------------------------------------------------------------------------------

clients_connection_list = []
clients_id_list = []
json_file_path = "data.json"


def server_program():
    # get the hostname
    host = '192.168.100.9'
    port = 800

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    tcp_server_socket.bind((host, port))  # bind host address and port together
    tcp_server_socket.listen(100)  # configure how many client the server can listen simultaneously

    print("======== Server Listening ======== ")
    while True:
        client, address = tcp_server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

        while True:

            data = client.recv(1024).decode("utf-8")  # receive data stream
            data = data.split('~')


            if data[0] == 'login_Request':
                email = data[1]
                password = data[2]
                client_id = Login_function(email, password)
                if client_id != 'User_Error':
                    print(f"login_Request:::---user: {email} ---pass: {password} ~Successful")

                    query_data = fetch_user_detal(client_id)
                    feed = f"{query_data[0]}~{query_data[1]}~{query_data[2]}~{query_data[3]}~{query_data[4]}~{query_data[6]}"
                    active_connections.update({client_id: [client, f"{query_data[1]} {query_data[1]} {query_data[1]}", f"{query_data[6]}"]})
                    client.send(str(feed).encode("utf-8"))
                else:
                    print(f"Connection from: {address} not approved -- disconnected")
                    client.send(str(client_id).encode("utf-8"))
                    client.close()
                    break
            elif data[0] == 'Sign_out_Request':
                client_id = data[1]
                print("Sign_out_Request:::---user id: ", client_id, " ~Successful")
                client.send(str('signed_out_success').encode("utf-8"))
                try:
                    del active_connections[client_id]
                except:
                    pass
                client.close()
                break
            elif data[0] == 'active':
                print(data[1])
                info = client.recv(int(data[1])).decode("utf-8")
                info = info.split("~")
                active_connections.update({info[0]: [client, info[1], info[2]]})
                print(active_connections)
                print("User added")

            elif data[0] == 'infoRequest':
                print(f"information_request by {address}")
                for user_info_key in active_connections:
                    print("sending")
                    user_id = user_info_key
                    user_name = active_connections[user_info_key][1]
                    user_profile = active_connections[user_info_key][2]
                    info = f"{user_id}~{user_name}~{user_profile}"
                    print(len(info))
                    client.send(str(len(info)).encode("utf-8"))
                    client.send(info.encode("utf-8")[:len(info)])

                client.send("end".encode("utf-8"))

                print(f"Information transaction to {address} Completed")


            elif data[0] == '':
                print("closing Connection for :", address)
                m = [key for key, value in active_connections.items() if value[0] == client]
                if len(m) != 0:
                    del active_connections[m[0]]
                client.close()
                break
            else:

                pass

if __name__ == '__main__':
          server_program()

