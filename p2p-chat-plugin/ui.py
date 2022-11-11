import threading
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from electroncash.i18n import _
from electroncash_gui.qt.util import MyTreeWidget, MessageBoxMixin

import sys
import time
sys.path.insert(0, '..')  # Import the files where the modules are located

from .MyOwnPeer2PeerNode import MyOwnPeer2PeerNode 
 
class Ui(MyTreeWidget, MessageBoxMixin):

    
    receive_message_trigger = pyqtSignal(str)
    receive_node_connection_trigger = pyqtSignal(str)

    def __init__(self, parent, plugin, wallet_name):
    
        # An initial widget is required.
        MyTreeWidget.__init__(self, parent, self.create_menu, [], 0, [])

        self.chat_history =""

        self.plugin = plugin
        self.wallet_name = wallet_name

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        #hbox1
        
        hbox1 = QHBoxLayout()
        self.main_power_switch = QCheckBox()
        self.main_power_switch.clicked.connect(self.process_main_power_switch)
        
        l = QLabel(_("Run chat module. When checked, your p2p node will run and accept incoming connections."))
        hbox1.addWidget(l)
        hbox1.addWidget(self.main_power_switch)
 
        hbox1b = QHBoxLayout() 
        self.node_status = QLabel(_("Node stopped."))
     
        l = QLabel(_("STATUS:"))
        hbox1b.addWidget(l)
        hbox1b.addWidget(self.node_status)
         
 
 
 
 
        l = QLabel(_("To connect to a friend, enter IP and port: "))
        
        
        
        
        self.ip_friend = QLineEdit()
        self.ip_friend.setMaximumWidth(70)
        self.port_friend = QLineEdit()
        self.port_friend.setMaximumWidth(70)
        self.connect_button = QPushButton(_("Connect"))
        # Disable connection UI for now (until connected)
        self.ip_friend.setEnabled(False)
        self.port_friend.setEnabled(False) 
        self.connect_button.setEnabled(False)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(l) 
        
        hbox2.addWidget(self.ip_friend)
        hbox2.addWidget(self.port_friend)
        hbox2.addWidget(self.connect_button)
        hbox2.addStretch(1)

        # Chat message and chat history widgets
        self.chatarea = QTextEdit()
        self.my_chat_msg = QLineEdit()
        self.message_button = QPushButton(_("Send Message"))
        # Disable chat for now (until connected)
        self.my_chat_msg.setEnabled(False)
        self.message_button.setEnabled(False)
        
        hbox3 = QHBoxLayout()
        self.connect_button.clicked.connect(self.connect)
        self.message_button.clicked.connect(self.send_msg)
        hbox3.addWidget(self.connect_button)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.my_chat_msg)
        hbox4.addWidget(self.message_button)
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.chatarea) 
        hbox2.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox1b)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
         
        # Set up triggers so we can call back into the ui from the p2pnetwork threads. 
        self.receive_message_trigger.connect(self.process_incoming_message)
        self.receive_node_connection_trigger.connect(self.process_node_connection) 
        
    def create_menu(self):
        pass

    def on_delete(self):
        pass

    def on_update(self):
        pass
        
    
    def connect(self):
        try:
            self.my_node.connect_with_node(self.ip_friend.text(), int(self.port_friend.text()))
            time.sleep(1)
        except:
            self.show_message(_("An error occured. Check your settings and try again."))
            
    def send_msg(self):
        self.my_node.send_to_nodes(str(self.my_chat_msg.text())) 
        #self.chat_history += "<font color=\"Green\">" +  str(self.my_chat_msg.text()) + "</font>"
        self.chat_history += str(self.my_chat_msg.text())
        self.chat_history += "\r\n" 
        self.chatarea.setText(self.chat_history)
        self.my_chat_msg.setText("")     
     
    # DEAL WITH INCOMING MESSAGES 
    def receive_chat_message(self,incoming_message):
        self.receive_message_trigger.emit(incoming_message)
        
    def process_incoming_message(self,incoming_message):
        self.chat_history += "\r\n" 
        self.chat_history += incoming_message
        self.chatarea.setText(self.chat_history) 
         
    # DEAL WITH NEW CONNECTION (incoming or outgoing)
    def receive_node_connection(self,node_id):
        print ("NEW CONNECTION, node id ",node_id)
        self.receive_node_connection_trigger.emit(str(node_id))
        
    def process_node_connection(self,node_id):
        print ("process node connection node id ",node_id)
        self.node_status.setText("Connected with node_id:"+node_id)
        self.ip_friend.setEnabled(False)
        self.port_friend.setEnabled(False)   
        self.connect_button.setEnabled(False)   
         
    def process_main_power_switch(self):
        print ("MAIN POWER IS NOW : ",self.main_power_switch.isChecked())
        if self.main_power_switch.isChecked():
            # Switch was just turned on, so start the node.
            try:
                self.my_node = MyOwnPeer2PeerNode("0.0.0.0", 8001, ui_window = self) 
                self.my_node.debug = True
                time.sleep(1)
                self.my_node.start() 
                self.node_status.setText("Node Started.")
                self.my_chat_msg.setEnabled(True)
                self.message_button.setEnabled(True)
                self.ip_friend.setEnabled(True)
                self.port_friend.setEnabled(True) 
                self.connect_button.setEnabled(True)
            except:
                self.show_message(_("An error occured. Socket may be in use. Please try again."))
        else:
            # Switch was just turned off, so stop the node.
            self.my_node.stop()
            self.node_status.setText("Node Stopped.")
            self.my_chat_msg.setEnabled(False)
            self.message_button.setEnabled(False)
            self.message_button.setEnabled(False)
            self.ip_friend.setEnabled(False)
            self.port_friend.setEnabled(False) 
            self.connect_button.setEnabled(False)

  
        
        
        
        
        
                            
