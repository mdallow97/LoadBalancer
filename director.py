# Director
import socket, pickle
import sys
import threading
import helper
import random

def updateLog(addr, specs):
    print("update")

def acceptUser():
    while 1:
        conn, addr = s.accept()

        if addr[0] in nodes:
            print("Connection activated from node with address ", addr)
            node_conns.append(conn)
        else:
            print("Connection from new user with address ", addr)
            users.append((conn, addr))

        recv_reqs_thread = threading.Thread(target=receiveRequest, args=(conn,addr))
        recv_reqs_thread.start()


def receiveRequest(conn, addr):
    data = None

    while not data:
        data = conn.recv(BUFFER_SIZE)

    x = pickle.loads(data)
    if type(x) == helper.MatrixCouple:
        x.setUser(addr)

        matrix_couple_queue.append(x)

    elif type(x) == helper.ResultMatrix:

        original_addr = x.getUser()
        for addr_tuple in users:
            print(addr_tuple[1], " vs ", original_addr)
            if addr_tuple[1] == original_addr:
                addr_tuple[0].send(pickle.dumps(x))
                break
        else:
            print("Not able to send result back to user")

    elif type(x) == helper.CPUSpecifications:
        hw_specs_log.append((addr, x))
        
    else:
        print("ERROR")


def distributeLoad():
    while 1:
        if not matrix_couple_queue:
            # Queue is empty, wait
            continue

        # This is the algorithm to distribute work (balance load)
        # RIGHT NOW IT IS RANDOM
        if len(node_conns) == 0:
            print("No nodes available")
            continue


        index = random.randint(0, len(node_conns)-1)
        conn = node_conns[index]

        matrix_couple = matrix_couple_queue.pop()
        conn.send(pickle.dumps(matrix_couple))


# Get local host name (IP)
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 0
BUFFER_SIZE = 1024

users = []
nodes = []
node_conns = []
matrix_couple_queue = []
hw_specs_log = []

if len(sys.argv) < 2:
    print("Format: python director.py <node1> <node2> <node3> <etc.>")
    exit()



for i in range(1, len(sys.argv)):
    nodes.append(sys.argv[i])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(10)
port = s.getsockname()[1]

print("Director with address ", host, "and port ", port)

# Two threads: One for distributing load, another for receiving incoming requests
distribute_load_thread = threading.Thread(target=distributeLoad)
accept_new_user_thread = threading.Thread(target=acceptUser)

distribute_load_thread.start()
accept_new_user_thread.start()
