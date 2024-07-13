import helper
from source import DawnSimVis
from models.message import Message as MSG
from models.message_types import MessageTypes as MT

#
# ────────────────────────────────────────────────────────────────── I ──────────
#   :::::: S Y N C   B F S   N O D E : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────────────────────
#

ROOT = 0 

class SyncBFSNode(DawnSimVis.BaseNode):
    def init(self):
        """
        Initializes the SyncBFSNode instance.

        Initializes the following attributes:
        - neighbors: a set to store the neighbors of the node
        - parent: the parent node of the current node
        - layer: the layer of the node in the BFS tree
        - round: the round of the node in the BFS tree
        - childs: a set to store the child nodes of the current node
        - others: a set to store the nodes not in the current node's layer
        - receive_upcast: a list to store the message types to be received
        """
        self.neighbors = set()  # Set to store the neighbors of the node
        self.parent = None  # Parent node of the current node
        self.layer = None  # Layer of the node in the BFS tree
        self.round = 1  # Round of the node in the BFS tree
        self.childs = set()  # Set to store the child nodes of the current node
        self.others = set()  # Set to store the nodes not in the current node's layer
        self.receive_upcast = []  # List to store the message types to be received

    def run(self):
        """
        Run the node's Breadth-First Search (BFS) algorithm.

        The function sends a MSG with the message type HEARTBEAT to all nodes in the network.
        If the node is the ROOT node, it also sends a MSG with the message type LAYER to all nodes,
        incrementing the layer by 1.
        """
        # Send HEARTBEAT message to all nodes
        self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.HEARTBEAT, None, self.id))

        # If the node is the ROOT node, send LAYER message to all nodes
        if self.id == ROOT:
            self.layer = 0
            self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.LAYER, self.layer + 1, self.id))

    def on_receive(self, msg: MSG):
        """
        This method is executed when the node receives a message.

        Args:
            msg (MSG): The received message packet.

        Returns:
            None
        """
        # Count received messages
        helper.msg_count += 1

        # Handle the received message based on its type
        if msg.type == MT.HEARTBEAT:
            # If the message type is HEARTBEAT, add the sender to the neighbors set
            self.neighbors.add(msg.src)
        elif msg.type == MT.LAYER:
            # If the message type is LAYER, execute the on_layer_receive method
            self.on_layer_receive(msg.val, msg.src)
        elif msg.type == MT.ACK:
            # If the message type is ACK, execute the on_ack_receive method
            self.on_ack_receive(msg.src)
        elif msg.type == MT.REJECT:
            # If the message type is REJECT, execute the on_reject_receive method
            self.on_reject_receive(msg.src)
        elif msg.type == MT.ROUND:
            # If the message type is ROUND, execute the on_round_receive method
            self.on_round_receive(msg.val, msg.src)
        elif msg.type == MT.UPCAST:
            # If the message type is UPCAST, execute the on_upcast_receive method
            self.on_upcast_receive(msg.val, msg.src)
        else:
            # If the message type is unknown, log an error message
            self.log(f"Unknown message type: {msg.type}")

    def on_layer_receive(self, l, j):
        """
        Handle the received LAYER message.

        Args:
            l (int): The layer value of the received message.
            j (int): The ID of the sender of the message.

        Returns:
            None
        """
        # If the node is a child of the root node and it receives a LAYER message,
        # it sets its own layer to the received layer value and sets its parent to the sender.
        # It then sends an ACK message to the parent node.
        # If the node is not a child of the root node, it sends a REJECT message to the sender.
        try:
            if self.parent is None and self.id != ROOT:
                self.layer = l
                self.parent = j
                self.send(self.parent, MSG(MT.ACK, None, self.id))
            else: 
                self.send(j, MSG(MT.REJECT, None, self.id))
        except Exception as e:
            # If an error occurs, log the error message with the details of the error.
            self.log(f":: x :: Error on layer: {l} from {j} | Error: {e}")

    def on_ack_receive(self, j):
        """
        This method is executed when the node receives an ACK message.

        Args:
            j (int): Sender's node id.

        Returns:
            None
        """
        try:
            # Add the sender node to the set of child nodes
            self.childs.add(j)

            # If the node is the root node
            if self.id == ROOT:
                # If the set of children and the set of neighbours are the same
                if self.childs == self.neighbors:
                    # Send a ROUND message to all nodes
                    self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.ROUND, self.round, self.id))
            else:
                # If the union of the Children and Others set is the same as the Neighbours set
                if self.neighbors == (self.childs | self.others):
                    # Send an UPCAST message to the parent node indicating whether the node is the last node in its subtree
                    self.send(self.parent, MSG(MT.UPCAST, True if self.childs == {} else False, self.id))

        except Exception as e:
            # If an error occurs, log the error message with the details of the error
            self.log(f":: x :: Error on ACK from {j} | Error: {e}")

    def on_reject_receive(self, j):
        """
        This method is executed when the node receives a REJECT message.

        Args:
            j (int): Sender's node id.

        Returns:
            None
        """
        try:
            # Add the rejected node to the list of "others"
            self.others.add(j)
            
            if self.id == ROOT:
                # If the node is the root and all the child nodes have been rejected,
                # send a new ROUND message to all nodes
                if self.childs == self.neighbors:
                    #self.log("ROOT düğüm Yeni ROUND mesajı yayınlanıyor.")
                    self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.ROUND, self.round, self.id))
            else:
                # If the node is not the root and all the child nodes have been rejected,
                # send an UPCAST message to the parent indicating that the node is not the last node in its subtree
                if self.neighbors == (self.childs | self.others):
                    self.send(self.parent, MSG(MT.UPCAST, True if self.childs == {} else False, self.id))
        
        except Exception as e:
            # Log any errors that occur during the execution of the method
            self.log(f":: x :: Error on REJECT from {j} | Error: {e}")

    def on_round_receive(self, r, j):
        """
        This method is executed when the node receives a ROUND message.

        Args:
            r (int): Round number.
            j (int): Sender's node id.

        Returns:
            None
        """
        try: 
            # Check if the received round is the same as the current layer
            if r == self.layer:
                # If the received round is the same as the current layer,
                # send a new LAYER message with the next layer
                self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.LAYER, self.layer + 1, self.id))
            else:
                # If the received round is not the same as the current layer,
                # check if the node has any child nodes
                if not self.childs:
                    # If the node has no child nodes, send an UPCAST message to the parent
                    self.send(self.parent, MSG(MT.UPCAST, True, self.id))
                else:
                    # If the node has child nodes, send the ROUND message to each child node
                    for child in self.childs:
                        self.send(child, MSG(MT.ROUND, r, self.id))
        except Exception as e:
            # Log any errors that occur during the execution of the method
            self.log(f":: x :: Error on ROUND({r}) from {j} | Error: {e}")

    def on_upcast_receive(self, f, j):
        """
        This method is executed when the node receives an UPCAST message.

        Args:
            f (bool): Upcast flag indicating whether the node is the last node in its subtree.
            j (int): Sender's node id.

        Returns:
            None
        """
        try:
            # Store the received upcast flag in the list.
            self.receive_upcast.append(f)

            # Check if all the received upcast flags are True.
            if len(self.receive_upcast) == len(self.childs):
                if all(self.receive_upcast):
                    # If the node is not the root, send an UPCAST message to its parent.
                    if self.id != ROOT:
                        self.send(self.parent, MSG(MT.UPCAST, True, self.id))
                    else:
                        # If the node is the root, indicate that the synchronous BFS algorithm has finished.
                        helper.last_time = self.now
                        helper.stop_sync_sim()
                        
                else:
                    # If not all the received upcast flags are True, perform the necessary actions.
                    if self.id == ROOT:
                        # Increment the round number and send a ROUND message to all nodes.
                        self.round += 1
                        self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.ROUND, self.round, self.id))
                    else:
                        # Send an UPCAST message to the parent indicating that the node is not the last node in its subtree.
                        self.send(self.parent, MSG(MT.UPCAST, False, self.id))
                
                # Reset the receive_upcast list.
                self.receive_upcast = []
        except Exception as e:
            # Log any errors that occur during the execution of the method.
            self.log(f":: x :: Error on UPCAST({f}) from {j} | Error: {e}")

#
# ──────────────────────────────────────────────────────────────────── II ──────────
#   :::::: A S Y N C   B F S   N O D E : :  :   :    :     :        :          :
# ──────────────────────────────────────────────────────────────────────────────
#

class AsyncBFSNode(DawnSimVis.BaseNode):
    def init(self):
        """
        Initialize the AsyncBFSNode class.

        This method initializes the following instance variables:
        - neighbors: a set to store the neighbors of the node.
        - parent: a variable to store the parent node.
        - layer: a variable to store the layer of the node. It is initialized as infinity.
        - childs: a set to store the child nodes.
        - others: a set to store the other nodes.
        """
        self.neighbors = set()  # Set to store the neighbors of the node.
        self.parent = None  # Variable to store the parent node.
        self.layer = float('inf')  # Variable to store the layer of the node. Initialized as infinity.
        self.childs = set()  # Set to store the child nodes.
        self.others = set()  # Set to store the other nodes.

    def run(self):
        """
        Initialize the node by sending a heartbeat message to all nodes.
        If the node is the root, it also sends a layer message to all nodes.

        This method does not take any parameters.

        This method does not return anything.
        """
        # Send a heartbeat message to all nodes.
        self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.HEARTBEAT, None, self.id))

        # If the node is the root, it sends a layer message to all nodes.
        if self.id == ROOT:
            self.layer = 0
            self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.LAYER, self.layer + 1, self.id))

    def on_receive(self, msg: MSG):
        """
        Handle incoming messages for the node.

        This method handles different types of messages received by the node.
        It performs the following actions based on the message type:
        - HEARTBEAT: Add the source node to the list of neighbors.
        - LAYER: Call the on_layer_receive method with the layer value and source node.
        - ACK: Call the on_ack_receive method with the source node.
        - REJECT: Call the on_reject_receive method with the source node.
        - Any other type: Log an error message indicating the unknown message type.

        Args:
            msg (MSG): The incoming message packet.

        Returns:
            None
        """
        # Increment the message counter
        helper.msg_count += 1

        # Handle the received message based on its type
        if msg.type == MT.HEARTBEAT:
            # Add the source node to the list of neighbors
            self.neighbors.add(msg.src)

        elif msg.type == MT.LAYER:
            # Call the on_layer_receive method with the layer value and source node
            self.on_layer_receive(msg.val, msg.src)

        elif msg.type == MT.ACK:
            # Call the on_ack_receive method with the source node
            self.on_ack_receive(msg.src)

        elif msg.type == MT.REJECT:
            # Call the on_reject_receive method with the source node
            self.on_reject_receive(msg.src)

        else:
            # Log an error message indicating the unknown message type
            self.log(f"Unknown message type: {msg.type}")

    def on_layer_receive(self, l, j):
        """
        Handle the received LAYER message.

        Args:
            l (int): The layer value of the received message.
            j (int): The ID of the sender of the message.

        Returns:
            None
        """
        try:
            # If the received layer value is less than the current layer value,
            # set the new layer value, parent node, and send ACK message to the parent node.
            # Also, send a new LAYER message to all nodes.
            if l < self.layer:
                if self.parent is not None:
                    self.send(self.parent, MSG(MT.REJECT, None, self.id))
                self.layer = l
                self.parent = j
                self.send(self.parent, MSG(MT.ACK, None, self.id))
                self.send(DawnSimVis.BROADCAST_ADDR, MSG(MT.LAYER, self.layer + 1, self.id))
            # If the received layer value is greater than or equal to the current layer value,
            # send a REJECT message to the sender.
            else:
                self.send(j, MSG(MT.REJECT, None, self.id))

        except Exception as e:
            # If an error occurs, log the error message with the details of the error.
            self.log(f":: X :: Error on layer {l} from {j}: Error is {e}")

    def on_ack_receive(self, j):
        """
        Handle the received ACK message.

        Args:
            j (int): The ID of the sender of the message.

        Returns:
            None
        """
        # Remove the sender node from the set of other nodes
        self.others.discard(j)
        # Add the sender node to the set of child nodes
        self.childs.add(j)

    def on_reject_receive(self, j):
        """
        Handle the received REJECT message.

        Args:
            j (int): The ID of the sender of the message.

        Returns:
            None
        """
        # Remove the sender node from the set of child nodes
        self.childs.discard(j)
        # Add the sender node to the set of other nodes
        self.others.add(j)
        # Update the last time with the current time
        helper.last_time = self.now
