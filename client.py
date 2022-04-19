import socket
import errno
from socket import error as socket_error
import argparse
import time
from xmlrpc import client
from cmath import sqrt

# UNCOMMENT THE LINES 11-15 AND COMMENT THE ONES FROM 17-21 TO MAKE IT WORK ON PI

# HOST = "10.35.70.28"  # The server's hostname or IP address
# PORT = 33333  # The port used by the server

# HOST2 = "10.35.70.41"
# PORT2 = 33343

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 33333  # The port used by the server

HOST2 = "127.0.0.1"
PORT2 = 33343


cert = b"invalid_pass"


# below is cmd line arg to take in client details

parser = argparse.ArgumentParser(description="Client help menu!")
""""
parser.add_argument("--n", default="admin",help="TUse this to enter clients name Usage: --a=Name")
parser.add_argument("--a", default="admin",help="Use this to enter clients age Usage: --a=Age")
parser.add_argument("--h", default="admin",help="Use this to enter clients heartrate Usage: --a=Heartrate")
parser.add_argument("--l", default="5658",help="Use this to enter listening port Usage: --a=Heartrate")


args = parser.parse_args()
client_name = args.n
client_addy = args.a
client_port = args.h
listening_port = int(args.l)

"""
parser.add_argument("--t", default="1",
                    help="Use this to run client testing Usage: --a=1")
args = parser.parse_args()
client_profile = args.t

# below is simple testing profiles to speed up running client so info does not need to be entered each time.

if client_profile == "1":
    client_name = "Max Lynch"
    client_addy = "123 Muffin Ave A96AX54"
    client_port = "#33010"
    listening_port = 33010

if client_profile == "2":
    client_name = "Sarah Dowley"
    client_addy = "21 Victoria Lawn A87AX32"
    client_port = "#33019"
    listening_port = 33019

if client_profile == "3":
    client_name = "Paraic O Reilly"
    client_addy = "44 Booterstown Road A83AX99"
    client_port = "#33012"
    listening_port = 33012

# Below is a function which calculates nearest hopsital server to connect to. The locations of these hopsitals are preprogrammed into our client - hopsital
# locations do not change quickly!

HospitalX = [4, 6, 7]
HospitalY = [3, 6, 4]
# for debugging all connect to same port, NEEDS TO BE CHANGED
HospitalPorts = [33001, 33001, 33001]

mindist = []

catch_flag = 0
cf2 = 0
cf3 = 0


def nearest_hospital(coords_list):
    for i in range(len(HospitalX)):
        eq = (HospitalX[i] - coords_list[0]) ^ 2 + \
            (HospitalY[i] - coords_list[1]) ^ 2
        sq = abs(sqrt(eq))

        mindist.append(sq)
       # print("Distance is calculated as: ")
       # print(mindist[i])

    index_min = min(range(len(mindist)), key=mindist.__getitem__)

    return index_min


client_data = client_port + " " + client_name + " " + client_addy
coords = input("Please enter your current coordinates: ")

coords = coords.split()
coords_int = [int(x) for x in coords]
hospital_port_index = nearest_hospital(coords_int)


while True:

    server_choice = input(
        "Please enter what mode you would like to access (L/R): ")

    if server_choice == "L":

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            try:
                s2.connect((HOST2, HospitalPorts[hospital_port_index]))
            except socket.error:
                print("This Hospital is offline, please restart the application")
                break

            s2.sendall(b"L")
            time.sleep(1)
            # below, client is sending port and data to NH
            print("Sending port number to nearest hospital.\n")

            s2.sendall(str(listening_port).encode("utf-8"))
            time.sleep(1)
            print("Sending Client Data to nearest hospital\n")
            s2.sendall(client_data.encode("utf-8"))

        # needs to go into listening mode now in case it needs to update list

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
                print("Socket now connecting to listen on port: " +
                      str(listening_port))
                s3.bind((HOST, listening_port))
                # print("binded")
                s3.listen()
                # print("listening")
                conn, addr = s3.accept()

                with conn:
                    print(f"Connected by {addr}")

                    init_b = conn.recv(1024)
                    init = init_b.decode("utf-8")

                    if init == "Sending file...":
                        print("Recieving file from NH")
                        with open("client_" + str(listening_port) + ".txt", "w") as f:
                            l = conn.recv(1024)
                            l_str = l.decode("utf-8")
                            while l_str:
                                f.write(l_str)
                                l = conn.recv(1024)
                                l_str = l.decode("utf-8")
                            f.close()

                    if init == "Emergency Resp...":
                        print("Neighbouring client has sent emergency response!")

                        em_data = conn.recv(1024)
                        em_data = em_data.decode("utf-8")
                        print("Client details, please repsond as soon as possible!:")
                        print(em_data)

                    if init == "Emergency Resp 2...":
                        flag = 0
                        print("Neighbouring client has sent emergency response!")

                        em_data = conn.recv(1024)
                        em_data = em_data.decode("utf-8")
                        print("Client details, please repsond as soon as possible!:")
                        print(em_data)

                        l = []
                        for line in open("client_" + str(listening_port) + ".txt", "r"):
                            l.append(line.split()[0][1:])

                        for i in range(len(l)):

                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                                try:
                                    print("Connecting to " + str(l[i]))
                                    s2.connect((HOST2, int(l[i])))
                                except socket.error:
                                    print(
                                        "Client at port " + str(l[i]) + " is offline, contacting next neighbour")
                                    flag = 1

                                if flag == 0:
                                    print(
                                        "Informing neighbour of emergency response details...")

                                    s2.sendall(b"Emergency Resp...")

                                    time.sleep(1)

                                    s2.sendall(em_data.encode("utf-8"))

                                    s2.close()

                                if flag == 1:
                                    flag = 0

    if server_choice == "R":  # registration mode for elderly people, will get a list from the hopsital but not enter listening mode- allowing them
        # to send an emergency signal to all

        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                try:
                    s2.connect((HOST2, HospitalPorts[hospital_port_index]))
                except socket.error:
                    print("This Hospital is offline, please restart the application")
                    break

                ## below, client is sending port and data to NH
                print("Sending port number to nearest hospital.\n")

                s2.sendall(str(listening_port).encode("utf-8"))
                time.sleep(1)
                print("Sending Client Data to nearest hospital\n")
                s2.sendall(client_data.encode("utf-8"))

        ## updates list and then allows client to enter emergency repsonse if necessary

        """
        while True:
            user_choice = input(
                "Enter if you would like to update your neighbour list or send an SOS (U/S): ")

            if user_choice == "U":
                print("U")

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    try:
                        print("Connecting to hospital to update list...")
                        s2.connect((HOST2, HospitalPorts[hospital_port_index]))
                        catch_flag = 0
                    except socket.error:
                        print("This Hospital is offline, please try again later")
                        catch_flag = 1

                    s2.sendall(b"U")

                    print("Recieving file from NH")
                    with open("client_" + str(listening_port) + ".txt", "w") as f:
                        l = s2.recv(1024)
                        l_str = l.decode("utf-8")
                        while l_str:
                            f.write(l_str)
                            l = s2.recv(1024)
                            l_str = l.decode("utf-8")
                        f.close()

            if user_choice == "S":
                print("Attempting to contact GP and neighbours: ")

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    try:
                        print("connecting")
                        s2.connect((HOST2, HospitalPorts[hospital_port_index]))
                        catch_flag = 0
                    except socket.error:
                        print(
                            "This Hospital is offline, attempting to connect to neighbour")
                        catch_flag = 1
                        cf3 = 0
                        cf2 = 0

                    if catch_flag == 0:  # hosp online, contact hospital

                        print("GP Online, contacting GP")

                        s2.sendall(b"S")

                        time.sleep(1)

                        s2.sendall(str(listening_port).encode("utf-8"))

                        time.sleep(1)

                        s2.sendall(client_data.encode("utf-8"))

                    if catch_flag == 1:  # hosp offline, contact client list
                        l = []
                        for line in open("client_" + str(listening_port) + ".txt", "r"):
                            l.append(line.split()[0][1:])

                        for i in range(len(l)):

                            if cf3 == 0:

                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                                    try:
                                        if l[i] == listening_port:
                                            print("")

                                        else:
                                            print("Connecting to " + str(l[i]))
                                            s2.connect((HOST2, int(l[i])))
                                            cf3 = 1
                                    except socket.error:
                                        print(
                                            "Client at port " + str(l[i]) + " is offline, contacting next neighbour")
                                        cf2 = 1

                                    if cf2 == 0:
                                        print(
                                            "Informing neighbour of emergency response details...")

                                        s2.sendall(b"Emergency Resp 2...")

                                        time.sleep(1)

                                        s2.sendall(client_data.encode("utf-8"))

                                        s2.close()

                                    if cf2 == 1:
                                        cf2 = 0

       # s.close
