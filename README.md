3 main components:
- User: Sends requests to the leader
- Director: Receives requests and forwards request depending on load balancing algorithm
- Computation Node: Where the  computation is sent to by the director and actually processed

Dataflow when user sends request (PART 1):
Connect to Director –> send 2 matrices –> consult load balancing algorithm –> send to chosen Computation Node –> multiply 2 matrices and respond to Director with the result –> forward result back to User

Dataflow when Computation Node becomes active (PART 2):
Connect to director –> provide director with HW Specifications –> Director adds node to log, will now be considered for computations


Current Functionality (5/28/19):
Connect to Director –> send 2 matrices –> randomly select computation node [$] and send 2 matrices –> computation node does the multiplication, prints to stdout for debugging purposes –> sends result back to Director, Director prints it –> [$$]

[$]: This should be changed from random to whatever load balancing alg we choose. The alg should depend on computation nodes hardware, which means we can't implement this part until PART 2 is complete (director needs hw specifications)

[$$]: I cannot seem to get the result from the leader back to the user (final step of PART 1)


Instructions on How to Run:
NOTE: This program will not work flawlessly because it is so far designed to be implemented across multiple machines (but has not been tested on multiple machines)

1) Run "python director.py <list_of_computation_node_IPs>"
2) Run "python computation_node.py <director_IP> <director_port>". The director's IP and Port will be printed after step 1. Step 2 should be run once at the very least, and as up to as many times as IPs included in the list in step 1.
3) Run "python user.py <director_IP> <director_port>". This can be run on multiple different machines like step 2, but not on the same machines as step 2. This will prompt you to enter a matrix size, which creates two matrices of the given size randomly
