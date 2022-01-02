
from queue import Queue
import socket
import threading
import json
import time
import hashlib


class node:
    
    data = list()
    finger_list = [None] * 160
    req_data = None
    queue1 = Queue()
    def __init__(self, ip, port):
        
        self.ip = ip  # returns the ip of localhost
        self.port = port  # port number
        # generates the ID of node using hash algorith
        self.id = self.getHashedID(ip, port)
        self.successor = None
        self.predecessor = None
        self.Lock = threading.Lock()
        self.thread = threading.Thread(target=self.run, args=(self.queue1,self.port,self.ip,))  # creates a thread to run the node
        self.thread.start()  # starts the thread

    def run(self, queue1,port,ip):  # run () is the function that proccess is executing when you run the thread.start()


        HOST, PORT = ip, port
        # Create socket instance, AF_INET refers to the address-family ipv4.
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The SOCK_STREAM means connection-oriented TCP protocol.
        # Set option for socket to reuseaddress for different ports
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the ip and the port of the socket
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(10)  # clients we can listen
        #thread_stabilize = threading.Timer(3,target=self.stabilize(),args=())
        
        while True:
            # enables the connection and waits for requests
            client_connection, client_address = listen_socket.accept()
            request_data = client_connection.recv(1024)  # recieves the request
            request_data = json.loads(request_data.decode('utf-8'))
            #print("before:", request_data)
            command = request_data["command"]

            if command == "find_successor":
                result = self.find_successor(request_data["id"])
                if(result["found"]):
                    request_data.update(result)
                    request_data["command"] = "rcv_data"
                    self.sendData(request_data["s_ip"],
                                  request_data["s_p"], request_data)
                else:
                    self.sendData(self.successor["ip"],self.successor["port"],request_data)

            if command == "get_predecessor" :
                result = self.predecessor
                result.update({"command":"rcv_data"})
                self.sendData(request_data["s_ip"],request_data["s_p"],result)
            

            if command == "notify":
                self.notify(request_data)
            
            if command == "rcv_data":
                queue1.put(request_data)
                
            if command == "shutdown":
                break

            client_connection.close()  # terminate the connection when message send

    def sendData(self, host, port, data):

        data = json.dumps(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            sock.sendall(bytes(data, encoding="utf-8"))
        finally:
            sock.close()

    

    def find_successor(self, id):
        
        
        if(id > self.id and id <= self.successor["id"]):
            return {"found": 1, "id": self.successor["id"], "ip": self.successor["ip"], "port": self.successor["port"]}
        else:
            return {"found": 0, "ip": self.successor["ip"], "port": self.successor["port"]}

    def get_successor(self, id):
        self.sendData(self.ip, self.port, data={"command": "find_successor", "id": id, "s_ip": self.ip, "s_p": self.port})
        time.sleep(2)
        response = self.queue1.get()
        self.req_data = response
        return response

    def join(self, node):
        response = self.get_successor(node.id)
        time.sleep(0.1)
        node.successor = {"id":response["id"],"ip":response["ip"],"port":response["port"]}

    
    def stabilize (self):
        
        time.sleep(2)
        data = {"command":"get_predecessor","s_ip":self.ip,"s_p":self.port}
        self.sendData(self.successor["ip"],self.successor["port"],data)
        time.sleep(2)
        response = self.queue1.get()
        predecessor_id = response["id"]
        if(predecessor_id> self.id and predecessor_id<self.successor["id"]):
            self.successor = {"id":response["id"],"ip":response["ip"],"port":response["port"]}
        
        data = {"command":"notify","id":self.id,"ip":self.ip,"port":self.port}
        self.sendData(self.successor["ip"],self.successor["port"],data)

    def notify(self,node):
        if(self.predecessor==None or (node["id"]>self.predecessor["id"] and node["id"]<self.id)):
            self.predecessor = node


    def getHashedID(self, ip, port):  # hashind data for id
        input = ip+str(port)
        hashobj = hashlib.sha256(input.encode())
        id = hashobj.hexdigest()
        id = int(id, 16)
        return id

    def getNodeInfo(self):  # returns the ip and port of node
        return self.ip, self.port, self.id

    def shutdown(self):  # terminates the proccess which node is running, we shutdown node
        self.sendData(self.ip, self.port, {"command": "shutdown"})