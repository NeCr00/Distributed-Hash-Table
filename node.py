import socket

class node:

    
    def __init__(self,ip,port):
        
        self.ip = ip #returns the ip of localhost
        self.port = port #port number
        self.id = self.getHashedID(ip,port)
        self.createNode(ip,port)
        

    def getHashedID(self,ip,port):
        id = hash(ip+str(port))
        return id

    def createNode(self,ip,port):

        HOST, PORT = ip, port

        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)
        
        while True:
            client_connection, client_address = listen_socket.accept()
            request_data = client_connection.recv(1024)
            print(request_data.decode('utf-8'))

            http_response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
            client_connection.sendall(http_response.encode())
            client_connection.close()


    def getNodeInfo (self):
        return self.ip,self.port
    

    
