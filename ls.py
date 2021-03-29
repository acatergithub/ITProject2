import threading
import time
import random
import socket
import sys
import select

def ls():
#borrowed code from ts.py need to change.
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Client/Server socket created")
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts1.setblocking(False)
        print("[S]: Server/ts1 socket created")
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts2.setblocking(False)
        print("[S]: Server/ts2 socket created")

    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = (sys.argv[1], int(sys.argv[2]))
    print(sys.argv[1])
    client.bind(server_binding)
    client.listen(5)
    server_binding = (sys.argv[3], int(sys.argv[4]))
    ts1.connect(server_binding)
    server_binding = (sys.argv[5], int(sys.argv[6]))
    ts2.connect(server_binding)

    while (True):
        (csockid, addr) = client.accept()
        print("[S]: Got a connection request from a client at {}".format(addr))
        #Data is recieved, decoded,set to lower, and all new lines are removed.
        data = csockid.recv(1000)
        data = data.decode("UTF-8", "strict")
        data = data.replace("\n", "")
        print("[S]: The requested domain is: ", data)
        #Now to call both ts severs and wait 5 seconds for a response.
        inputs = [ts1,ts2]
        outputs = [ts1,ts2]
        info = ""
        while inputs and info == "":
            readable,writeable,errors = select.select(inputs,outputs,inputs,0.5)
            for i in writeable:
                print("Sending, ", data)
                i.send(data.encode("UTF-8","strict"))
                outputs.remove(i)
            for i in readable:
                info = i.recv(1024)
                inputs.remove(i)
                client.send(info)
                break
            for i in errors:
                print("ERROR")
                inputs.remove(i)
                outputs.remove(i)
                break


    # Close the server socket

    ls.close()
    exit()

ls()