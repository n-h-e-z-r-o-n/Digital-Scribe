import socket
import cv2
import numpy as np

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #server_ip = socket.gethostbyname(socket.gethostname()) #"127.0.0.1"  # replace with the server's IP address

    server_ip = "139.84.228.75"

    server_port = 800  # replace with the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        a_bytes = frame.tobytes()

        client.send(str(len(a_bytes)).encode("utf-8")[:1024])
        client.send(str(frame.shape).encode("utf-8")[:1024])
        client.send(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cap.destroyAllWindows()

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()
