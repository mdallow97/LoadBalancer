# user.py
import socket, pickle
import sys
import random
import helper
import time
import threading

def sendMatrice(index):
    filename = "matrix-dir/" + test_names[index]

    t0 = time.time()
    matrix_file = open(filename, "rb")
    file_data = matrix_file.read()
    helper.send_msg(s, file_data)

    data = helper.recv_msg(s)
    result = pickle.loads(data)

    t1 = time.time()
    print("Time to multiply matrices of size ", result.getSize(), ": ", t1-t0)



test_names = ["matrix16", "matrix128", "matrix256", "matrix512", "matrix1024", "matrix2048", "matrix4096"]

if len(sys.argv) != 3:
    print("Format: python user.py <Director_IP> <Director_Port>")
    exit()

director_IP = sys.argv[1]
director_port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((director_IP, director_port))

print("Run tests? (y/n): ")
reply = input()

if reply == 'n':
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
        helper.send_msg(s, pickle.dumps(matrix_set))

        data = helper.recv_msg(s)
        result = pickle.loads(data)

        print("\n\tResulting Matrix")
        helper.printMatrix(result.getResult(), result.getSize())
else:
    print("How many test files (out of 7): ")
    num_tests = int(input())

    if num_tests > 7:
        print("No more than 7 tests")
        exit()

    _matrices_threads = []
    for i in range(num_tests):
        matrice_thread = threading.Thread(target=sendMatrice, args=(i,))
        send_matrices_threads.append(matrice_thread)
        matrice_thread.start()

    for thread in send_matrices_threads:
        thread.join()
