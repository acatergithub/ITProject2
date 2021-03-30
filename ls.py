import threading
import time
import random
import socket
import sys
import select
import time

def ls():
#borrowed code from ts.py need to change.
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Client/Server socket created")
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server/ts1 socket created")
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server/ts2 socket created")

    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', int(sys.argv[1]))
    print(sys.argv[1])
    client.bind(server_binding)
    client.listen(5)
    server_binding = (sys.argv[2], int(sys.argv[3]))
    ts1.connect(server_binding)
    server_binding = (sys.argv[4], int(sys.argv[5]))
    ts2.connect(server_binding)
    ts1.setblocking(False)
    ts2.setblocking(False)

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
        start = time.time()
        end = False
        #Loop for checking non blocking recv calls. Will end when data is recieved, inputs empties, or 5 seconds have passed.
        while inputs and info == "":
            print("how often does it get here?")
            readable, writeable, exceptional = select.select(inputs,outputs,inputs,0.5)
            print(len(readable))
            for i in writeable:
                print("Sending, ", data)
                i.send(data.encode("UTF-8","strict"))
                outputs.remove(i)
            print(len(readable))
            for i in readable:
                print("Checking!")
                info = i.recv(1024)
                print("Data Recieved!")
                inputs.remove(i)
                csockid.send(info)
                break

            for i in exceptional:
                print("ERROR")
                inputs.remove(i)
                outputs.remove(i)
                break
            if (time.time() - start) >= 5:
                end = True
                break
        print("Left loop")
        if end:
            print("NO HOST")
            ret = "- Error:HOST NOT FOUND"
            csockid.send(ret.encode("UTF-8","strict"))

    # Close the server socket

    ls.close()
    exit()

ls()