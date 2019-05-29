# user.py
import socket, pickle
import sys
import random
import helper

if len(sys.argv) != 3:
    print("Format: python user.py <Director_IP> <Director_Port>")
    exit()

BUFFER_SIZE = 1024
director_IP = sys.argv[1]
director_port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((director_IP, director_port))

while 1:
    # Get input matrix from stdin (assume all matrices are square [nxn])
    # Package matrix into class
    # Send matrices to director
    # Wait for response from director

    print("Enter N for the two NxN matrices to be multiplied: ")
    size = input()

    if size == "exit":
        exit()

    n = int(size)
    matrix1 = [[0] * n for i in range(0, n)]
    matrix2 = [[0] * n for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            matrix1[i][j] = random.randint(0, 500)
            matrix2[i][j] = random.randint(0, 500)

    print("\n\tMatrix A")
    helper.printMatrix(matrix1, n)
    print("\n\n\n\tMatrix B\n")
    helper.printMatrix(matrix2, n)

    matrix_set = helper.MatrixCouple(matrix1, matrix2, n)
    s.send(pickle.dumps(matrix_set))


    # NOT ABLE TO SEND DATA BACK YET
    data = None
    while not data:
        data = s.recv(BUFFER_SIZE)

    result = pickle.loads(data)
    helper.printMatrix(result.getResult(), result.getSize())
