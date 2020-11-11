from dataclasses import dataclass

# TODO:
#   Add documentation.


class Matrix(tuple):

    def __init__(self, matrix: tuple):
        if Matrix.is_valid_matrix(matrix):
            self.matrix = matrix

    def is_matrix(func):
        def wrapper(*xs):
            if type(xs[1]) is not Matrix:
                raise TypeError("Argument should be of Matrix type.")

            return func(*xs)
        return wrapper

    def is_int(func):
        def wrapper(*xs):
            if type(xs[1]) is not int:
                raise TypeError("Argument should be of int type.")

            return func(*xs)
        return wrapper

    def __len__(self):
        return len(self.matrix)

    def __str__(self):
        return "%s" % (self.matrix,)

    def __repr__(self):
        return "Matrix(%s)" % (self.matrix,)

    def __neg__(self):
        return Matrix(tuple(tuple(-item for item in row) for row in self))

    @is_matrix
    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("Matrix must be of the same order.")

        if self is other:
            return self * 2

        return Matrix(tuple(tuple((sum(cell_pair) for cell_pair in zip(s_row, o_row)))
                            for s_row, o_row in zip(self, other)))

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Matrix(tuple(tuple(cell * other for cell in row) for row in self))

        elif type(other) is Matrix:
            if len(self) != len(other):
                raise ValueError("Matrix must be of the same order.")

            return Matrix(tuple(tuple(sum(s_cell * o_cell for s_cell, o_cell in zip(s_row, o_col))
                                      for o_col in zip(*other)) for s_row in self))

        else:
            raise TypeError("Argument should be of int or float or Matrix type.")

    def __rmul__(self, other):
        return self * other

    @is_matrix
    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        if type(other) is not int and type(other) is not float:
            raise TypeError("Argument should be of int or float type.")

        return Matrix(tuple(tuple(cell / other for cell in row) for row in self))

    @is_matrix
    def __eq__(self, other):
        if len(self) != len(other):
            return False

        if self is other:
            return True

        if any(s_row != o_row for s_row, o_row in zip(self, other)):
            return False

        return True

    def __ne__(self, other):
        return not self == other

    def __getitem__(self):
        for row in self.matrix:
            yield row

    def __hash__(self):
        return hash(row for row in self)

    @property
    def tuples(self):
        print("%s" % (self.matrix,))

    @classmethod
    def is_valid_matrix(cls, matrix: tuple):
        if any(type(row) is not tuple for row in matrix):
            raise TypeError("All rows should be tuples")

        if any(any(type(item) is not int and type(item) is not float for item in row) for row in matrix):
            raise TypeError("Cells should be numbers")

        if any(len(matrix) != len(row) for row in matrix):
            raise ValueError("Number of rows and columns should be the same")

        return True

    @classmethod
    @is_int
    def unity(cls, number: int = 0):
        if number < 0:
            raise ValueError("Argument should be of positive value.")

        return cls(tuple(tuple(1 if i == j else 0 for i in range(number)) for j in range(number)))

    @classmethod
    @is_int
    def ones(cls, number: int = 0):
        if number < 0:
            raise ValueError("Argument should be of positive value.")

        return cls(tuple((tuple((1,) * number),) * number))


# Temporery testing section:
a = Matrix(((1, 1, 1), (2, 2, 2), (3, 3, 3)))
b = Matrix(((4, 4, 4), (5, 5, 5), (6, 6, 6)))
c = Matrix(((1, 1, 1), (2, 3, 1), (0, 2, 0)))

# print(a)
#
# print(repr(a))
#
# a.tuples
#
# print(Matrix.unity(3))
#
# print(Matrix.ones(3))
#
# print(a + b)
# print(a + c)
# print(b + a)
# print(c + a)
# print(a + a)
# print(a + Matrix.unity(3))
# print(a + ((1,),))

# print(a - b)
# print(b - a)
# print(a - c)
# print(c - a)
# print(a - a)
# print(a - Matrix.unity(3))
# print(a - ((1,),))

# print(10 * a)
# print(10.1 * a)
# print(a * 10)
# print(a * 10.1)
# print(a / 10)
# print(a / 10.1)

a = Matrix(((1, 2), (3, 4)))
b = Matrix(((3, 5), (6, 8)))

# print(a * b)
# print(b * a)
# print(a * a)

# print(a == b)
# print(a != b)
# print(a == a)
# print(a != a)

# b = Matrix(((1, 2), (3, 4)))
# print(a == b)
# print(a != b)

# for i in a:
#     print(str(i))

# dictionary = {}
# dictionary[Matrix(((1, 1), (2, 2)))] = 1
# dictionary[Matrix(((1, 1), (2, 2)))] = 2
# dictionary[Matrix(((1, 1), (2, 3)))] = 3
# print(dictionary)