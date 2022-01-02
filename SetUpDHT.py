
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

def create_Ring(node):
    node.successor = {"id":node.id,"ip":node.ip,"port":node.port}
    node.predecessor = None

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
    create_Ring(nodes[0])

    nodes[0].join(nodes[1])
    while True:
        selection = print_menu()
        
        if(selection == '7'):
            terminate(nodes)


if __name__ == '__main__':
    print("---------------------- Welcome to Distributed Hash Tables ----------------------\n")
    main()
