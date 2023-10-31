import socket
import hashlib
import select

# ---------------------- creating a connection to the database.---------------------------------------------------------
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12hezron12",
    database="menta_application_schema"
)
cursor = mydb.cursor()


# ========================================================== FUNCTIONS DEFINITIONS ==========================================================
# ---------------------- function to encrypt userdata. --------------------------------------------------------------------------------------
def encryp(string):
    salt = "5gzbella"
    string = string + salt  # Adding salt to the password
    hashed = hashlib.md5(string.encode())  # Encoding the password
    return hashed.hexdigest()  # return the Hash


# ---------------------- function to validate login credentials. ----------------------------------------------------------------------------

def Login_function(Email, password):
    cursor.execute("select * from users_type2 where Email=%s and Password=%s", (Email, encryp(password)))
    query_result = cursor.fetchall()
    if len(query_result) == 0:
        return 'User_Error'
    else:
        return query_result[0][0]


# -----------------------------------------------------------------------------------------------------------------------

clients_connection_list = []
clients_id_list = []
def server_program():
    # get the hostname
    host = '127.0.0.1'
    port = 800

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    tcp_server_socket.bind((host, port))  # bind host address and port together
    tcp_server_socket.listen(100)     # configure how many client the server can listen simultaneously

    print("Server Listening")
    while True:
        client, address = tcp_server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

        while True:
            data = client.recv(1024).decode("utf-8")  # receive data stream
            data = data.split('~')
            print(data)

            if data[0] == 'login_Request':
                email = data[1]
                password = data[2]
                client_id = Login_function(email, password)
                if client_id != 'User_Error':
                    client.send(str(client_id).encode("utf-8"))
                    clients_connection_list.append(client)
                    clients_id_list.append(str(client_id))
                else:
                    client.send(str(client_id).encode("utf-8"))
                    client.close()
                    break
            elif data[0] == 'Sign_out_Request':
                index = clients_id_list.index(data[1])
                clients_connection_list[index].send(str('signed_out_success').encode("utf-8"))
                clients_connection_list[index].close()
                print(clients_id_list)
                print(clients_id_list[index])
                print(clients_id_list)
                print(clients_connection_list[index])
                del clients_id_list[index]
                del clients_connection_list[index]
                break
            else:
                pass





if __name__ == '__main__':
    server_program()
    m = Login_function("m@gmail", '12maureen12')
    print(m)
