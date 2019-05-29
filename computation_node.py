# Computation Node
import socket, pickle
import sys
import helper

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


if len(sys.argv) != 3:
    print("Format: python computation_node.py <Director_IP> <Director_Port>")
    exit()


BUFFER_SIZE = 1024
director_IP = sys.argv[1]
director_port = int(sys.argv[2])

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
