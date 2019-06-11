import socket, pickle
import random
from helper import MatrixCouple

index = 0
sizes = [16, 128, 256, 512, 1024, 2048, 4096]

for size in sizes:
	matrix1 = [[0] * size for i in range(0, size)]
	matrix2 = [[0] * size for i in range(0, size)]

	for i in range(0, size):
		for j in range(0, size):
			matrix1[i][j] = random.randint(0, 8192)
			matrix2[i][j] = random.randint(0, 8192)

	matrix_set = MatrixCouple(matrix1, matrix2, size, index)

	filename = "matrix" + str(size)
	outfile = open(filename, "wb")
	outfile.write(pickle.dumps(matrix_set))
	outfile.close()
	index += 1
