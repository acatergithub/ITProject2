import threading
import time
import random
import socket
import sys

def ts():

    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    with open("PROJI-DNSTS.txt") as DNS:
        DNSList = [line.rstrip('\n').split(" ", 1) for line in DNS]  # Reads from the file

    print(DNSList)

    serverList = {}
    for i in range(len(DNSList) - 1):
        serverList[DNSList[i][0]] = []  # Creates the dictionary severList from the DNS 2d array
        serverList[DNSList[i][0]].append(DNSList[i][1])
        print(serverList[DNSList[i][0]])

    server_binding = ('', int(sys.argv[1]))
    print(sys.argv[1])
    ts.bind(server_binding)
    ts.listen(5)

    while (True):
        (csockid, addr) = ts.accept()
        print("[S]: Got a connection request from a client at {}".format(addr))

        data = csockid.recv(1000)
        data = data.decode("UTF-8", "strict")
        data = data.replace("\n", "")

        print("[S]: The requested domain is: ", data)
        print("[S]: The sent address is: ", serverList.get(data.lower(), "localhost - NS"))
       # if data in serverList:
        #    print(serverList[data.lower()])
         #   csockid.send(serverList[data.lower()][0].encode('utf-8'))
       # else:
        #    csockid.send("- Error:HOST NOT FOUND".encode('utf-8'))
        if data in serverList:
            print(serverList[data.lower()])
            csockid.send(serverList[data.lower()][0].encode('utf-8'))
        else:
            csockid.send("- Error:HOST NOT FOUND".encode('utf-8'))
        time.sleep(5)

    # Close the server socket

    ts.close()
    exit()

ts()