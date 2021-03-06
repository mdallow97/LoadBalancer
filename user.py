# user.py
import socket, pickle
import sys
import random
import helper
import time
import threading

from helper import ResultMatrix
from time import sleep

exec_time = []
# Threaded function that receives results
def recvMatrice(s, i):

    data = helper.recv_msg(s)
    result = pickle.loads(data)

    t1 = time.time()
    print("Time to multiply matrices", i, " of size ", result.getSize(), ": ", t1-result.getTime())

    exec_time.append(t1-result.getTime())

def createRandOrder(rng):
    flags = []
    order = []
    for i in range(0, rng):
        flags.append(0)
        order.append(-1)

    num_flags_activated = 0
    while num_flags_activated < rng:
        index = random.randint(0, rng-1)

        if flags[index] == 1:
            continue
        else:
            order[num_flags_activated] = index
            flags[index] = 1
            num_flags_activated += 1

    return order

# File names that contain raw matrice data
test_names = ["matrix16", "matrix128", "matrix256", "matrix512", "matrix1024", "matrix2048", "matrix4096"]

if len(sys.argv) != 3:
    print("Format: python user.py <Director_IP> <Director_Port>")
    exit()

# Connect to director
director_IP = sys.argv[1]
director_port = int(sys.argv[2])


# For testing purposes?
print("Run tests? (y/n): ")
reply = input()

if reply == 'n':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((director_IP, director_port))
    while 1:
        # Get matrix size from stdin (assume all matrices are square [nxn])


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

        # Package matrix into class and send matrices to director
        matrix_set = helper.MatrixCouple(matrix1, matrix2, n, "-1")
        helper.send_msg(s, pickle.dumps(matrix_set))

        # Wait for response from director
        data = helper.recv_msg(s)
        result = pickle.loads(data)

        print("\n\tResulting Matrix")
        helper.printMatrix(result.getResult(), result.getSize())
else:
    # Ask how many files to test
    print("How many test files (out of 7): ")
    num_tests = int(input())

    if num_tests > 7 or num_tests < 1:
        print("ERROR: Invalid number of tests")
        exit()

    send_matrice_threads = []
    return_sockets = []
    order = createRandOrder(num_tests)
    print("Order: ", order)
    for i in order:
        # Create socket for each matrix set
        return_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_socket.connect((director_IP, director_port))
        return_sockets.append(return_socket)

        # Locate matrix file (raw data), forward to director
        filename = "matrix-dir/" + test_names[i]
        t0 = time.time()
        matrix_file = open(filename, "rb")
        file_data = matrix_file.read()
        matrice = pickle.loads(file_data)
        matrice.setTime(t0)
        file_data = pickle.dumps(matrice)
        helper.send_msg(return_socket, file_data)

        # Start thread that will receive result
        matrice_thread = threading.Thread(target=recvMatrice, args=(return_socket, i))
        send_matrice_threads.append(matrice_thread)
        matrice_thread.start()

    # When done, join threads and close connections
    mean_exec_time = 0
    for i in range(num_tests):
        send_matrice_threads[i].join()
        return_sockets[i].close()
        mean_exec_time += exec_time[i]

    # Calculate mean execution time
    print("===========RESULT===========")
    print("Mean Execution Time: ", mean_exec_time/num_tests)
    print("Number of tests: ", num_tests)
