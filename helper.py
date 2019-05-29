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
    def __init__(self, rank):
        # instead of rank, can have clock frequency, # cores, # processors, # GPUs, etc
        self.rank = rank;

    def getRank(self):
        return self.rank


def printMatrix(matrix, n):
    for i in range(n):
        print("\n")
        for j in range(n):
            print(matrix[i][j], end=" ")
    print("\n\n")

# Will later do parsing of hw specifications
