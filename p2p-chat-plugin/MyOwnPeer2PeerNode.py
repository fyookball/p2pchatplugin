"""MyOwnPeer2PeerNode is an example how to use the p2pnet.Node to implement your own peer-to-peer network node.
Change Log:
28/06/2021: Added the new developments on id and max_connections"""


#from .p2pnetwork.node import Node
from . import p2pnetwork
Node = p2pnetwork.node.Node

class MyOwnPeer2PeerNode(p2pnetwork.node.Node):
    def __init__(self, host, port, id=None, callback=None, max_connections=0, ui_window=None):
        super(MyOwnPeer2PeerNode, self).__init__(host, port, id, callback, max_connections)
        self.ui_window=ui_window
    # All the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        self.ui_window.receive_node_connection(str(node.id)[0:9])

    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)
        self.ui_window.receive_node_connection(str(node.id)[0:9])

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        print("node_message (" + self.id + ") from " + node.id + ": " + str(data))
        self.ui_window.receive_chat_message(str(data))

    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)

    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")
