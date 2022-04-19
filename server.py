from cmath import sqrt
from http import client
import socket
import argparse
import time


# THIS SERVER RECIEVES CLIENT CODE AFTER COMM WITH DEFAULT SERVER

# UNCOMMENT THE LINES 12-16 AND COMMENT THE ONES FROM 18-22 TO MAKE IT WORK ON PI

# HOST = "10.35.70.41"  # Standard loopback interface address (localhost)
# PORT = 33001  # Port to listen on (non-privileged ports are > 1023)

# HOST2 = "10.35.70.28"
# PORT2 = 33339

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 33001  # Port to listen on (non-privileged ports are > 1023)

HOST2 = "127.0.0.1"
PORT2 = 33339


parser = argparse.ArgumentParser(
    description="Authentication Server help menu!")
parser.add_argument("--a", default="admin",
                    help="This is the ID used to start the Final Count on the counting server. Usage: --a=PASSWORD")

args = parser.parse_args()
admin_pass = args.a

client_port_list = []

catch_flag = 0


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            operation_b = conn.recv(1024).decode("utf-8")
            operation = str(operation_b)

            # below is if statement that lets our clinet send L or S so server knows how to react to incoming connection
            print("Client wants to access " + operation + " mode")
            if operation == "L":

                print("IN L")

                # recieves port first
                client_port_b = conn.recv(1024)
                client_port = int(client_port_b.decode("utf-8"))
                print("Adding " + str(client_port) + " to client port list")
                client_port_list.append(client_port)

                print("Current Client Port List:")
                for i in range(len(client_port_list)):

                    print(client_port_list[i])

                # then recieves client data
                client_data_b = conn.recv(1024)
                client_data = str(client_data_b.decode("utf-8"))
                print(client_data)

                with open("hospital_" + str(PORT) + ".txt", "a") as f:
                    f.write(client_data + "\n")
                    f.close()

                for i in range(len(client_port_list)):

                    print("i = " + str(i))
                    catch_flag = 0
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                        try:
                            print("Connecting to " + str(client_port_list[i]))
                            s2.connect((HOST2, client_port_list[i]))
                        except socket.error:
                            print("Client at port " + str(client_port) +
                                  " is offline, please restart the application")
                            catch_flag = 1

                        if catch_flag == 0:
                            print("Attempting to send updated file to client...")

                            s2.sendall(b"Sending file...")
                            with open("hospital_" + str(PORT) + ".txt", "r") as f2:
                                l = f2.read(1024)

                                while (l):
                                    print("Sending file")
                                    l_encode = l.encode("utf-8")
                                    s2.sendall(l_encode)
                                    l = f2.read(1024)
                                f2.close()

                            s2.close()

                        if catch_flag == 1:
                            catch_flag = 0

            if operation == "S":

                print("Client has issued emergency response!")

                em_port = conn.recv(1024)
                em_port = int(em_port.decode("utf-8"))
                em_data = conn.recv(1024)
                #em_data = str(em_data_b.decode("utf-8"))

                print("Contacting neighbours of client for first repsonse aid!")

                for i in range(len(client_port_list)):

                    print("i = " + str(i))
                    catch_flag = 0
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                        try:
                            print("Connecting to " + str(client_port_list[i]))
                            s2.connect((HOST2, client_port_list[i]))
                        except socket.error:
                            print("Client at port " + str(client_port) +
                                  " is offline, contacting next neighbour")
                            catch_flag = 1

                        if catch_flag == 0:
                            print(
                                "Informing neighbour of emergency response details...")

                            s2.sendall(b"Emergency Resp...")

                            time.sleep(1)

                            s2.sendall(em_data)

                            s2.close()

                        if catch_flag == 1:
                            catch_flag = 0

            if operation == "U":

                print("Attempting to send updated file to client...")

                time.sleep(1)

                with open("hospital_" + str(PORT) + ".txt", "r") as f2:
                    l = f2.read(1024)

                    while (l):
                        print("Sending file")
                        l_encode = l.encode("utf-8")
                        conn.sendall(l_encode)
                        l = f2.read(1024)
                    f2.close()

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    try:
                        s2.connect((HOST2, 3213))
                    except socket.error:
                        print("Reboot")

                    s2.close()

    s.close()
    time.sleep(5)

    # parse through list and update all clients that have connected thus far with new client list

    # at this point, NH will have read in new client

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:

    # conn.sendall(nearest_hospital_index)
