# -*- coding: utf-8 -*-

# Copyright 2013, Patrick Poitras (acebulf at gmail dot com)
# License : Creative Commons Attribution 3.0 Unported (CC BY 3.0)

"""
The LabData module is composed primarily of a class called LabData, whose primary goal is
to allow for calculations on error propagation of the type commonly used in undergraduate
science lab reports.

Use of this module is simple;

    *First, define a variable as LabData(value, error) where value and error are most often
    represented in writing as {value} ± {error}. NOTE: Error is the absolute error and not
    the relative error.

        -> For relative uncertainties, the format is LabData(value, relative_error, r=True);
            it will then be converted to absolute uncertainty on __init__.

        -> Relative uncertainties are defined as (error / value)

        -> If the uncertainty is provided as a string including exactly one instance of "%" it
            will also be treated like a relative uncertainty, and a percentage, so its value will be
            divided by 100.

    *Then, all operations can be done like they would be using integers/floats/Decimal;

    Supported operations:
        + - / *

    Examples:

        Basic operations:

    >>> x = LabData(10,1) # 10 ± 1
    >>> print(x + 5)
    15 ± 1
    >>> y = LabData(10,5) # 10 ± 5
    >>> print(x + y)
    20 ± 6
    >>> print(x - y)
     0 ± 6
    >>> print(x * y)
    100 ± 60
    >>> print(x / y)
    1 ± 0.6
    >>> (x / y).printrel()
    1 ± 60%

        Using a tuple for operations/relative uncertainties:
    >>> y = (10, 5)
    >>> print(x + y)
    20 ± 6
    >>> y = (10, 0.5, True)
    >>> print(x - y)
    0 ± 6
    >>> y = (10, "50%")
    >>> print(x * y)
    100 ± 60
    >>> y = LabData(10, "50%", False)  # When the uncertainty is given as a string with "%", the r parameter is ignored
    >>> print(x / y)
    1 ± 0.6


"""

__author__ = 'Acebulf'
from decimal import Decimal, DecimalException

#todo - implement sig figs.
    #todo - possibly make __len__() return the number of sig figs


class LabData:
    print_unicode = True  # If true will print the unicode ± instead of +/-

    def __init__(self, value, incert, r=False):
        self.value = Decimal(value)

        if not isinstance(r, bool):
            raise TypeError('r (3rd value provided) must be a bool, indicating if the previous value ' +
                            'is a relative uncertainty or not')

        if (r is False and (not isinstance(incert, str))) or (isinstance(incert, str) and incert.count("%") == 0):
            # Handles relative uncertainties
            self.incert = abs(Decimal(incert))
            if self.value == Decimal(0):
                self.relative = 0
            else:
                self.relative = self.incert / self.value  # Needed for * and /

        elif isinstance(incert, str) and incert.count("%") == 1:
            self.relative = abs(Decimal(self.__string_rem(incert))) / 100
            self.incert = self.relative * self.value

        elif r is True:
            self.relative = abs(Decimal(incert))
            self.incert = self.relative * self.value

        else:
            ValueError("Could not parse uncertainty.")

    def __string_rem(self, other):  # Function to remove "%" from uncertainty
        if not isinstance(other, str):
            raise TypeError("The function string_rem is an internal function for formatting " +
                            "and must only be used on str instances.")
        ret_str = ""
        for x in other:
            if x != "%":
                ret_str += x
        return ret_str

    def __add__(self, other):  # Add
        new_incert = self.incert

        if isinstance(other, LabData):
            new_value = self.value + other.value
            new_incert = self.incert + other.incert

        elif isinstance(other, (int, str, float, Decimal)):
            new_value = self.value + Decimal(other)

        elif isinstance(other, tuple):  # default handling for tuple is direct conversion to LabData
            if len(other) == 2:  # no r-parameter provided
                oth_val, oth_inc = other
                other_LD = LabData(oth_val, oth_inc)
                return self + other_LD

            elif len(other) == 3:  # check for r parameter
                oth_val, oth_inc, oth_r = other
                if isinstance(oth_r, bool):
                    other_LD = LabData(oth_val, oth_inc, oth_r)
                    return self + other_LD

                else:
                    raise ValueError("Could not parse tuple.")

            else:
                raise NotImplementedError("No support for tuple of supplied length")

        else:
            raise TypeError("No operation for provided type")

        return LabData(new_value, new_incert)

    def __sub__(self, other):  # Subtract
        new_incert = self.incert

        if isinstance(other, LabData):
            new_value = self.value - other.value
            new_incert += other.incert

        elif isinstance(other, (int, str, float, Decimal)):
            new_value = self.value - Decimal(other)

        elif isinstance(other, tuple):
            if len(other) == 2:
                oth_val, oth_inc = other
                oth_LD = LabData(oth_val, oth_inc)
                new_value = self.value - oth_LD.value
                new_incert += oth_LD.incert

            elif len(other) == 3:  # check for r parameter
                oth_val, oth_inc, oth_r = other
                if isinstance(oth_r, bool):
                    other_LD = LabData(oth_val, oth_inc, oth_r)
                    return self - other_LD

                else:
                    raise ValueError("Could not parse tuple.")

            else:
                raise NotImplementedError("No support for tuple of supplied length")

        else:
            raise TypeError("No operation for type in class LabData")

        return LabData(new_value, new_incert)

    def __addinverse__(self):
        """
        Returns the additive inverse of self (self*-1)
        """
        if self.value != 0:
            return LabData(self.value * -1, self.incert)
        else:
            return LabData(self.value, self.incert)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return (self - other).__addinverse__()

    def __mulinverse__(self):
        """
        Returns the multiplicative inverse. (1/self)
        """
        return LabData(Decimal(1) / self.value, self.relative, r=True)

    def __mul__(self, other):

        if isinstance(other, LabData):
            new_value = self.value * other.value
            new_incert_r = self.relative + other.relative

        elif isinstance(other, (int, str, float, Decimal)):
            new_value = self.value * Decimal(other)
            new_incert_r = self.relative

        elif isinstance(other, tuple):
            if len(other) == 2:
                oth_val, oth_inc = other
                oth_LD = LabData(oth_val, oth_inc)
                new_value = self.value * oth_LD.value
                new_incert_r = self.relative + oth_LD.relative

            elif len(other) == 3:
                oth_val, oth_inc, oth_r = other
                if not isinstance(oth_r, bool):
                    raise ValueError("Could not parse tuple.")
                oth_LD = LabData(oth_val, oth_inc, oth_r)
                new_value = self.value * oth_LD.value
                new_incert_r = self.relative + oth_LD.relative

            else:
                raise NotImplementedError("There is no definition for a tuple of provided length")

        else:
            raise TypeError("Could not parse type for multiplication")

        return LabData(new_value, new_incert_r, r=True)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, LabData):
            new_value = self.value / other.value
            new_incert_r = self.relative + other.relative

        elif isinstance(other, (str, int, float, Decimal)):
            new_value = self.value / Decimal(other)
            new_incert_r = self.relative

        elif isinstance(other, tuple):
            if len(other) == 2:
                oth_val, oth_inc = other
                oth_LD = LabData(oth_val, oth_inc)
                new_value = self.value / oth_LD.value
                new_incert_r = self.relative + oth_LD.relative

            elif len(other) == 3:
                oth_val, oth_inc, oth_r = other
                if not isinstance(oth_r, bool):
                    raise ValueError("Could not parse tuple.")
                oth_LD = LabData(oth_val, oth_inc, oth_r)
                new_value = self.value / oth_LD.value
                new_incert_r = self.relative + oth_LD.relative

            else:
                raise NotImplementedError("There is no definition for a tuple of provided length")
        else:
            raise TypeError("Could not parse type for division")

        return LabData(new_value, new_incert_r, r=True)

    def __rdiv__(self, other):
        return (self / other).__mulinverse__()

    def __repr__(self):
        return "LabData(" + str(self.value) + ',' + str(self.incert) + ')'

    def __str__(self):
        #todo - Implement sig figs when object is printed
        if self.print_unicode is True:
            return (unicode(str(self.value)) + " " + u"\u00B1" + " " + unicode(str(self.incert))).encode("utf-8")
        else:
            return str(self.value) + " +/- " + str(self.incert)

    def printrel(self, is_unicode=None):  # Print with relative uncertainty
        if is_unicode is None:  # If unicode is none, it will default from self.print_unicode
            if self.print_unicode is False:
                return str(self.value) + " +/- " + str(self.relative * 100) + "%"
            else:
                return ((str(self.value) + " " + u"\u00B1" + " " + str(self.relative * 100) + "%")).encode("utf-8")
        elif is_unicode == "False" or is_unicode is False:
            return str(self.value) + " +/- " + str(self.relative * 100) + "%"
        else:
            return ((str(self.value) + " " + u"\u00B1" + " " + str(self.relative * 100) + "%")).encode("utf-8")

    def retrel(self, is_unicode=None):  # Return relative uncertainty as string
        if is_unicode is None:
            if self.print_unicode is False:
                return str(self.value) + " +/- " + str(self.relative * 100) + "%"
            else:
                return ((str(self.value) + " " + u"\u00B1" + " " + str(self.relative * 100) + "%")).encode("utf-8")

        elif (isinstance(is_unicode, bool) and is_unicode is False) or\
             (isinstance(is_unicode, str) and is_unicode.lower() == "false"):
            return str(self.value) + " +/- " + str(self.relative * 100) + "%"
        else:
            return ((str(self.value) + " " + u"\u00B1" + " " + str(self.relative * 100) + "%")).encode("utf-8")