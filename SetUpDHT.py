
from node import node
import argparse
import time


def arguments():
    # create Parser
    parser = argparse.ArgumentParser()
    # adding arguments
    parser.add_argument('--ip', type=str, required=True,
                        help='The host address')
    parser.add_argument('--port', type=int, required=True,
                        help='The start port number')
    parser.add_argument('--n', type=int, required=True,
                        help='The number of nodes')
    args = parser.parse_args()

    return args


def print_menu():
    print("------------------- Menu: -------------------\n")
    print("1 --> Insert Key\n")
    print("2 --> Delete Key\n")
    print("3 --> Query Key\n")
    print("4 --> Update Record Based on Key\n")
    print("5 --> Add Node\n")
    print("6 --> Delete Node\n")
    print("7 --> Exit\n")
    selection = input("Select an option --> ")

    return selection

def create_Ring(node1,node2):
    node1.successor = {"id":node2.id,"ip":node2.ip,"port":node2.port}
    node1.predecessor = {"id":node2.id,"ip":node2.ip,"port":node2.port}
    node2.successor = {"id":node1.id,"ip":node1.ip,"port":node1.port}
    node2.predecessor = {"id":node1.id,"ip":node1.ip,"port":node1.port}


def createNodes(ip, port, num_nodes):  # creates instances of class node
    nodes = []
    for i in range(num_nodes):

        nodes.append(node(ip, port+i))

    return nodes


def terminate(nodes):  # Terminates all the nodes and exiting from the main proccess

    for i in nodes:
        i.shutdown()

    print("Nodes Terminated ...")
    print("Exiting ...")
    exit()


def main():

    args = arguments()  # get correct arguments from command-line
    # ip address of nodes, starting port of nodes, number of nodes
    nodes = createNodes(args.ip, args.port, args.n)
    create_Ring(nodes[0],nodes[1])

    nodes[0].join(nodes[4])
    nodes[0].join(nodes[3])
    
    nodes[4].stabilize()
    nodes[3].stabilize()
    nodes[0].stabilize()
    nodes[1].stabilize()
    
    
    print(vars (nodes[0]),end="\n")
    print(vars (nodes[1]),end="\n")
    print(vars (nodes[4]),end="\n")
    print(vars (nodes[3]),end="\n")
    
    while True:
        selection = print_menu()
        
        if(selection == '7'):
            terminate(nodes)


if __name__ == '__main__':
    print("---------------------- Welcome to Distributed Hash Tables ----------------------\n")
    main()
