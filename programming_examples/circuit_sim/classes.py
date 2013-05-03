# -*- coding: utf-8 -*-

# Copyright 2013, Patrick Poitras (acebulf at gmail dot com)
# License : Creative Commons Attribution 3.0 Unported (CC BY 3.0)
class NodeContainer:
    """
    Container for nodes. Stores the nodes in a dictionary where the position is
    the key, represented as a tuple (x,y) or (x,y,z) and the value is a list of
    nodes at the position.
    """

    def __init__(self):
        self.container = {}
        if Node.container == None:
            Node.container = self  # Passes itself as a class variable to Node
        else:
            raise IndexError("Attempted to pass self to Node but Node already" +
                             "has container")

    def write(self, position, node, stack=False, nowarn=False):
        """
        write is used to write that a node object is present at a position.

        If a position does not yet exist, it will create it.

        If the node is already present at the position and stack == False, it
        will create a warning unless nowarn == True. The node will not be added
        to the position's list.

        If stack == True, the node will be added to the position regardless of
        whether it is present or not.
        """

        try:
            if (node not in self.container[position]) or stack:
                self.container[position].append(node)
            elif not nowarn:
                print("Warning: Node {!r} already present at position.").format(str(node))
                print("Node not stacked")
        except KeyError:
            self.container[position] = [node]

    def read(self, position):
        """
        Returns the list of nodes at position.
        """
        return self.container[position]

class Node:
    container = None
    def __init__(self, component, position):
        self.component = component
        self.position = position
        Node.container.write(position, self)

    def __str__(self):
        if self.instance != None:
            return self.component + str(self.instance)
        else:
            return self.component

class Component:
    """
    Master class for components.
    """

class Component_unordered(Component):
    """
    Component where the order of nodes is not important
    """
    def create_nodes(self, positions):
        """
        This creates and returns a list of nodes. To be used when
        node order is not important (eg. resistor)
        """
        nodes = []
        for pos in positions:
            nodes.append(Node(self, pos))
        return nodes

class Component_ordered(Component):
    """
    Component where the order of nodes is important
    """
    def create_nodes(self, positions):
        """
        When node order is important (volt. source, transistor, ect.)
        ordered_nodes will create a dictionary instead of a list with
        each node being stored under a name.

        Positions are passed as a list of tuple pairs (name, position)
        where name is the key that will be used in
        """
        nodes = {}
        for tup in positions:
            name, position = tup
            nodes[name] = Node(self, position)
        return nodes

class Resistor(Component_unordered):
    def __init__(self, resistance, positions):
        self.nodes = self.create_nodes(positions)
        self.resistance = resistance

class Voltage_Source(Component_ordered):
    """
    Voltage_Source has to have positions provided with
    keys 'positive' and 'ground' for node labeling.

    Emf is the electromotive force, in volts.
    """
    def __init__(self, emf, positions):
        self.emf = emf
        self.nodes = self.create_nodes(positions)

class Diode(Component_ordered):
    """
    Diodes will only let current pass from positive to
    negative. Has to have positions provided with keys
    'positive' and 'ground'.
    """
    def __init__(self, positions):
        self.nodes = self.create_nodes(positions)