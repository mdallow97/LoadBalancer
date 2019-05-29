# Parser

class MatrixCouple:
    def __init__(self, matrix1, matrix2, n, user_addr=None):
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.n = n

    def getMatrix1(self):
        return self.matrix1

    def getMatrix2(self):
        return self.matrix2

    def setUser(self, user):
        self.user = user

    def getUser(self):
        if self.user:
            return self.user

    def getSize(self):
        return self.n

class ResultMatrix:
    def __init__(self, result, n, user):
        self.result = result
        self.n = n
        self.user = user

    def getResult(self):
        return self.result

    def getSize(self):
        return self.n

    def getUser(self):
        return self.user

class Specifications:
    # can hold different hw specifications
    def __init__(self, num_CPUs, num_GPUs):
        # [0]: number processors, [1]: number cores, [2]: frequency
        self.CPU = []
        self.GPU = []

        self.CPU.append(num_CPUs)
        self.GPU.append(num_GPUs)

    def setCPUspecifics(self, frequency, num_cores):
        self.CPU.append(num_cores)
        self.CPU.append(frequency)

    def setGPUspecifics(self, frequency, num_cores):
        self.GPU.append(num_cores)
        self.GPU.append(frequency)

    def setMemorySize(self, mem_size):
        self.mem_size = mem_size

    def getMemorySize(self):
        return self.mem_size

    def getCPU(self):
        return self.CPU

    def getGPU(self):
        return self.GPU


def printMatrix(matrix, n):
    for i in range(n):
        print("\n")
        for j in range(n):
            print(matrix[i][j], end=" ")
    print("\n\n")

# Will later do parsing of hw specifications
