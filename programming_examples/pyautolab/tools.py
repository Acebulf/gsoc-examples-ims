# -*- coding: utf-8 -*-

# Copyright 2013, Patrick Poitras (acebulf at gmail dot com)
# License : Creative Commons Attribution 3.0 Unported (CC BY 3.0)

from pyautolab.classes import *

#todo - Documentation

def example_calc(arg1, arg2, operation, ret=False):  # performs a 2-variable calculation
    """
    example_calc is used to print an example of a calculation.

    If ret == True, it will also return the answer.
    """

    if not isinstance(operation, str):
        raise TypeError("Desired operation must be provided in string form")

    elif (not isinstance(arg1, LabData)) or (not isinstance(arg2, LabData)):
        raise TypeError("Arguments provided are not instances of LabData")

    elif operation == "+":
        print("({0}) + ({1})").format(str(arg1), str(arg2))

        print(str(arg1 + arg2))
        if ret is True:
            return arg1 + arg2

    elif operation == "-":
        print("({0}) - ({1})").format(str(arg1), str(arg2))
        print(str(arg1 - arg2))
        if ret is True:
            return arg1 - arg2

    elif operation == "*":
        print("({0}) X ({1})").format(str(arg1), str(arg2))
        print("({0}) X ({1})").format(str(arg1.retrel()), str(arg2.retrel()))

        print (arg1 * arg2).retrel()
        print (arg1 * arg2)
        if ret is True:
            return arg1 * arg2

    elif operation == "/":
        print("({0}) / ({1})").format(str(arg1), str(arg2))
        print("({0}) / ({1})").format(str(arg1.retrel()), str(arg2.retrel()))

        print(arg1 * arg2).retrel()
        print(arg1 * arg2)
        if ret is True:
            return arg1 / arg2


#TESTS
if __name__ == "__main__":
    x = LabData(10, 5)
    y = LabData(10, 1)

    example_calc(x, y, "+")
    print("\n\n")
    example_calc(x, y, "-")
    print("\n\n")
    example_calc(x, y, "*")
    print("\n\n")
    example_calc(x, y, "/")

