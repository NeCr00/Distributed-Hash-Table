import socket
from node import node
import argparse
import time

def print_menu ():
    print("------------------- Menu: -------------------\n")
    print ("1 --> Insert Key\n")
    print("2 --> Delete Key\n")
    print("3 --> Query Key\n")
    print("4 --> Update Record Based on Key\n")
    print("5 --> Add Node\n")
    print("6 --> Delete Node\n")
    selection = input("Select an option --> ")

    return selection

    
#create Parser
parser = argparse.ArgumentParser()
#adding arguments
parser.add_argument('--ip',type=str,required=True,help = 'The host address')
parser.add_argument('--port',type=int,required=True,help = 'The start port number')
parser.add_argument('--n',type=int,required=True,help = 'The number of nodes')
args = parser.parse_args()

print("---------------------- Welcome to Distributed Hash Tables ----------------------\n")

ip = args.ip #ip address of nodes
port = args.port #starting port of nodes
num_nodes = args.n #number of nodes

nodes = list()

for i in range(num_nodes):
    nodes.append(node (ip,port+i))




