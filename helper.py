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

class CPUSpecifications:
    # can hold different hw specifications
    def __init__(self, num_CPUs, num_cores, frequency):
        # [0]: number processors, [1]: number cores, [2]: frequency
        self.num_CPUs = num_CPUs
        self.num_cores = num_cores
        self.frequency = frequency

    def setMemorySize(self, mem_size):
        self.mem_size = mem_size

    def getMemorySize(self):
        return self.mem_size

class NodeInfo:
    # can hold different hw specifications
    def __init__(self, connection):
        # [0]: socket connection
        self.con = connection
        self.wt = 1.0
        self.jobs = []
        self.waiting = True

    def setWeight(self, weight):
        self.wt = weight

    def appendJob(self, job):
        self.jobs.append(job)

    def getWeight(self):
        return self.weight

    def getJobs(self):
        return self.jobs

    def getJobsSize(self):
        #calc combined weight of all jobs
        total = 0.0
        for i in jobs:
            total = total + float(jobs[i].getSize()) * (1.0 / float(self.getWeight()))
        return total

def printMatrix(matrix, n):
    for i in range(n):
        print("\n")
        for j in range(n):
            print(matrix[i][j], end=" ")
    print("\n\n")
