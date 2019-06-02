# Computation Node
from __future__ import print_function
from collections import OrderedDict
import pprint
import socket, pickle
import sys
import helper
import cpuinfo

from helper import Specifications

def multiplyMatrices(matrix_couple):
    n = matrix_couple.getSize()
    result = [[0] * n for i in range(0, n)]
    matrix1 = matrix_couple.getMatrix1()
    matrix2 = matrix_couple.getMatrix2()

    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result

'''
def getCPUinfo():
    \''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    cpu_info['proc0']={...}
    cpu_info['proc1']={...}

    \'''

    cpuinfo=OrderedDict()
    procinfo=OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs=nprocs+1
                # Reset
                procinfo=OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''

    return cpuinfo


def getSpecifications():

    cpuinfo = getCPUinfo()
    numCPUs = 0
    for processor in cpuinfo.keys():
        numCPUs += 1
        print(cpuinfo[processor]['model name'])

    print("Total number of processor: ", numCPUs)
'''

def getSpecifications():
    cpu_model = cpuinfo.cpu.info[0]['model name']
    cpu_cores = cpuinfo.cpu.info[0]['cpu cores']
    print("# processors?: ", len(cpuinfo.cpu.info))


if len(sys.argv) != 3:
    print("Format: python computation_node.py <Director_IP> <Director_Port>")
    exit()


BUFFER_SIZE = 1024
director_IP = sys.argv[1]
director_port = int(sys.argv[2])

hw_specs = getSpecifications()



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((director_IP, director_port))

# Get specifications
# Load into class
# Send to director so that it may update the log

while 1:
    data = s.recv(BUFFER_SIZE)
    if not data:
        continue

    matrix_couple = pickle.loads(data)

    if not type(matrix_couple) == helper.MatrixCouple:
        print("Received garbage")
        exit()

    result = multiplyMatrices(matrix_couple)
    return_val = helper.ResultMatrix(result, matrix_couple.getSize(), matrix_couple.getUser())

    s.send(pickle.dumps(return_val))
