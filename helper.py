# Parser
import struct

# Object type that will be sent to computation node
class MatrixCouple:
    def __init__(self, matrix1, matrix2, n, label, user_addr=None):
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.n = n
        self.time = 0
        self.label = label
        self.user = user_addr

    def getMatrix1(self):
        return self.matrix1

    def getMatrix2(self):
        return self.matrix2

    def setUser(self, user):
        self.user = user

    def setTime(self, time):
        self.time = time

    def getUser(self):
        if not self.user:
            return None
        else:
            return self.user

    def getTime(self):
        return self.time

    def getSize(self):
        return self.n

    def getLabel(self):
        return self.label

# Object type returned from computation node
class ResultMatrix:
    def __init__(self, result, n, label, user):
        self.result = result
        self.n = n
        self.user = user
        self.label = label

    def getResult(self):
        return self.result

    def getSize(self):
        return self.n

    def getUser(self):
        return self.user

    def setTime(self, time):
        self.time = time

    def getTime(self):
        return self.time

    def getLabel(self):
        return self.label

# Object type gathered by computation node and sent to director
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
        return self.wt

    def getJobs(self):
        return self.jobs

    def getJobsSize(self):
        #calc combined weight of all jobs
        total = 0.0
        for i in self.jobs:
            total = total + 2.0 * float(i.getSize() ** 2) * (1.0 / float(self.getWeight()))
        return total

# Used for sending very large messages
def send_msg(socket, msg):
    print("Bytes sent: ", len(msg))
    msg = struct.pack('>I', len(msg)) + msg
    socket.sendall(msg)

# Used for receiving very large messages
def recv_msg(socket):
    raw_msg_len = recvall(socket, 4)
    if not raw_msg_len:
        return None
    msglen = struct.unpack('>I', raw_msg_len)[0]
    data = recvall(socket, msglen)
    print("Bytes received: ", len(data))
    return data

# A helper function for receiving large messages
def recvall(socket, n):
    data = b''
    while len(data) < n:
        packet = socket.recv(n - len(data))
        if not packet: return None
        data += packet
    return data

# Prints a matrix
def printMatrix(matrix, n):
    for i in range(n):
        print("\n")
        for j in range(n):
            print(matrix[i][j], end=" ")
    print("\n\n")
