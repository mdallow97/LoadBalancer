# Director
import socket, pickle
import sys
import threading
import helper
import random

from helper import CPUSpecifications
from helper import NodeInfo

def updateSpecs(addr, specs):
    node_conns[addr[0]].setWeight(calcWeight(specs))

def acceptUser():
    while 1:
        conn, addr = s.accept()

        if addr[0] in nodes:
            print("Connection activated from node with address ", addr)
            #node_conns.append(conn)
            node_conns[addr[0]] = helper.NodeInfo(conn)
            print(list(node_conns))
        else:
            print("Connection from new user with address ", addr)
            users.append((conn, addr))

        recv_reqs_thread = threading.Thread(target=receiveRequest, args=(conn,addr))
        recv_reqs_thread.start()


def receiveRequest(conn, addr):
    data = helper.recv_msg(conn)

    print("Data Received!: ", len(data))
    x = pickle.loads(data)
    if type(x) == helper.MatrixCouple:
        x.setUser(addr)

        matrix_couple_queue.append(x)

    elif type(x) == helper.ResultMatrix:
        needJob(addr)
        original_addr = x.getUser()
        for addr_tuple in users:
            if addr_tuple[1] == original_addr:
                helper.send_msg(addr_tuple[0], pickle.dumps(x))
                print("Result sent back to user!")
                break
        else:
            print("Not able to send result back to user")

    elif type(x) == helper.CPUSpecifications:
        updateSpecs(addr, x)

    else:
        print("ERROR")

def calcWeight(specifications):
    w = 1.0
    w *= float(specifications.num_CPUs)
    w *= float(specifications.num_cores)
    w *= float(specifications.frequency)

    return w

def randomDist():
    return random.choice(list(node_conns))

def WLC():
    key = ""
    lowestLoad = float("inf")#initialize to pos infinity
    for i in list(node_conns):
        temp = node_conns[i].getJobsSize()
        if temp < lowestLoad:
            key = i
            lowestLoad = temp
    return key

def distributeLoad():
    while 1:
        if not matrix_couple_queue:
            # Queue is empty, wait
            continue

        if len(node_conns) == 0:
            print("No nodes available")
            continue

        # This is the algorithm to distribute work (balance load)
        # RIGHT NOW IT IS WLC
        key = WLC()

        matrix_couple = matrix_couple_queue.pop()
        node_conns[key].jobs.append(matrix_couple)
        sendNextJob(key)#TODO: this may need to be casted

def needJob(addr):
    node_conns[addr[0]].waiting = True
    sendNextJob(addr)

def sendNextJob(addr):
    if node_conns[addr[0]].waiting == True:
        if not len(jobs) == 0:
            conn = node_conns[addr[0]].conn
            job = jobs[0]
            jobs.pop()
            data = pickle.dumps(node_conns[addr[0]].jobs[0])
            helper.send_msg(conn, data)
            print("Bits sent to node: ", len(data))
            node_conns[addr[0]].waiting = False

# Get local host name (IP)
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 0

users = []
nodes = []
node_conns = {}
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
