import socket
import sys

def client(request, port, host ):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    #define the ts_port as the 4th arg
    ls_port = int(sys.argv[2])

    # get address of the host
    addr = sys.argv[1]

    # connect to the server using its address
    server_binding = (addr, port)
    cs.connect(server_binding)

    #encode request and send it to root server
    cs.send(request.encode('utf-8'))

    #recieve response, decode it
    response = cs.recv(100).decode('utf-8')

    #if the request is not found, return ERROR
    if response == "- Error:HOST NOT FOUND":
        return response

    #print("[C]: Data received from server: {}".format(data_from_server))

    data_from_server = response.split()

    #if the rs server respons with "localhost - NS" call client again on the


    # close the client socket
    cs.close()
    return response

def client_driver():

    rs_host_name = sys.argv[1]
    rs_port = int(sys.argv[2])

    print(rs_port)

    # open input folder and store lines in sites list
    with open('PROJ2-HNS.txt') as f:
        sites = f.readlines()

    outF = open("RESOLVED2.txt", "w")

    #List of thruples to store responses
    responses = list()

    #create connection and send request to RS for each website
    for site in sites:
        site = site.rstrip('\n')
        response = client(site,rs_port, rs_host_name)
        response = response.upper()
        outF.write(site)
        outF.write(" ")
        outF.write(response)
        outF.write("\n")
    outF.close()


client_driver()
