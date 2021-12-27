import socket
import multiprocessing
class node:

    data = list()

    def __init__(self,ip,port):
        
        
        self.ip = ip #returns the ip of localhost
        self.port = port #port number
        self.id = self.getHashedID(ip,port) #generates the ID of node using hash algorithm
        self.process = multiprocessing.Process(target=self.run, args=(self.ip,self.port)) #creates a process to run the node
        self.process.start() # starts the process
        
        

    def getHashedID(self,ip,port): #hashind data for id
        id = hash(ip+str(port))
        return id

    def run(self,ip,port): #run () is the function that proccess is executing when you run the process.start()

        HOST, PORT = ip, port
        
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Create socket instance, AF_INET refers to the address-family ipv4. 
        #The SOCK_STREAM means connection-oriented TCP protocol. 
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Set option for socket to reuseaddress for different ports
        listen_socket.bind((HOST, PORT)) #bind the ip and the port of the socket
        listen_socket.listen(1) # clients we can listen 
        
        while True:
            client_connection, client_address = listen_socket.accept() #enables the connection and waits for requests
            request_data = client_connection.recv(1024) #recieves the request
            #print(request_data.decode('utf-8'))
            http_response = 'HTTP/1.0 200 OK\n\n Node -->'+str(self.id) #http encoded message to print in web browser
            client_connection.sendall(http_response.encode()) #sends the message, access the request from browser, type ip:port on browser
            client_connection.close() #terminate the connection when message send


    def getNodeInfo (self): #returns the ip and port of node
        return self.ip,self.port
    

    def kill(self): #terminates the proccess which node is running, we shutdown node
       self.process.terminate()
