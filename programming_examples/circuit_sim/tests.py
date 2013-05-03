__author__ = 'Acebulf'

from classes import *
import string


if __name__ == "__main__":
    from random import randint, choice

    #NodeContainer tests with string as node
    node_ph = "".join(choice(string.ascii_uppercase) for x in xrange(1, randint(2, 40)))
    node_ph2 = "".join(choice(string.ascii_uppercase) for x in xrange(1, randint(2, 40)))
    print node_ph
    pos_ph = (randint(1, 100000), randint(1, 100000))
    container = NodeContainer()
    container.write(pos_ph, node_ph)
    assert container.read(pos_ph) == [node_ph]
    container.write(pos_ph, node_ph2)
    assert container.read(pos_ph).count(node_ph) == 1
    assert container.read(pos_ph).count(node_ph2) == 1


    assert container.read(pos_ph).count(node_ph) == 1
    assert container.read(pos_ph).count(node_ph2) == 1
    container.write(pos_ph, choice((node_ph, node_ph2)), stack=True)
    assert container.read(pos_ph).count(node_ph) + container.read(pos_ph).count(node_ph2) == 3