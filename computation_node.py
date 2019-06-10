# Computation Node
from __future__ import print_function
from collections import OrderedDict
import pprint
import socket, pickle
import sys
import helper
import cpuinfo
import helper

def multiplyMatrices(matrix_couple):
    n = matrix_couple.getSize()
    result = [[0] * n for i in range(0, n)]
    matrix1 = matrix_couple.getMatrix1()
    matrix2 = matrix_couple.getMatrix2()
    print("Working..")

    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    print("DONE")
    return result

def getSpecifications():
    # Get CPU information
    # Assumes all CPUs on one system are the same
    cpu_model = cpuinfo.cpu.info[0]['model name']
    cpu_cores = cpuinfo.cpu.info[0]['cpu cores']
    num_cpus  = len(cpuinfo.cpu.info)

    index = 0
    for i in range(len(cpu_model)):
        if cpu_model[i] == '@':
            index = i+1
            break

    clock_rate_str = ""
    for i in range(index, len(cpu_model)):
        if cpu_model[i] == 'G':
            break
        clock_rate_str += cpu_model[i]

    clock_rate = float(clock_rate_str)

    return helper.CPUSpecifications(num_cpus, cpu_cores, clock_rate)


if len(sys.argv) != 3:
    print("Format: python computation_node.py <Director_IP> <Director_Port>")
    exit()


director_IP = sys.argv[1]
director_port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((director_IP, director_port))

hw_specs = getSpecifications()
helper.send_msg(s, pickle.dumps(hw_specs))

# Get specifications
# Load into class
# Send to director so that it may update the log

while 1:
    data = helper.recv_msg(s)


    print("recieved data")
    matrix_couple = pickle.loads(data)

    if not type(matrix_couple) == helper.MatrixCouple:
        print("Received garbage")
        exit()

    result = multiplyMatrices(matrix_couple)
    return_val = helper.ResultMatrix(result, matrix_couple.getSize(), matrix_couple.getUser())

    helper.send_msg(s, pickle.dumps(return_val))
