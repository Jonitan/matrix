from typing import Union


class Matrix:

    def __init__(self, matrix: tuple):
        if type(matrix) is not tuple:
            raise TypeError("Matrix should be of tuple type.")
        self.is_valid_matrix(matrix)
        self.matrix = matrix

    @property
    def tuples(self):
        return self.matrix

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return f"Matrix({self.matrix})"

    def __len__(self):
        return len(self.matrix)

    def __getitem__(self, i):
        return self.matrix[i]

    def __hash__(self):
        return hash(self.matrix)

    def __neg__(self):
        return self * (-1)

    def __eq__(self, other):
        if type(other) is not Matrix:
            raise TypeError("Argument is not of Matrix type.")

        if len(self) != len(other):
            return False

        if self is other:
            return True

        if any(s_row != o_row for s_row, o_row in zip(self, other)):
            return False

        return True

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if type(other) is not Matrix:
            raise TypeError("Argument is not of Matrix type.")

        if len(self) != len(other):
            raise ValueError("Matrix must be of the same order.")

        if self is other:
            return self * 2

        return Matrix(tuple(tuple((sum(cell_pair) for cell_pair in zip(self_row, other_row)))
                            for self_row, other_row in zip(self, other)))

    def __sub__(self, other):
        if type(other) is not Matrix:
            raise TypeError("Argument is not of Matrix type.")

        return self + (-other)

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Matrix(tuple(tuple(cell * other for cell in row) for row in self))

        elif type(other) is Matrix:
            if len(self) != len(other):
                raise ValueError("Matrix must be of the same order.")

            return Matrix(tuple(tuple(sum(self_cell * other_cell for self_cell, other_cell in zip(self_row, other_col))
                                      for other_col in zip(*other)) for self_row in self))

        else:
            raise TypeError("Argument should be of int or float or Matrix type.")

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other: Union[int, float]):
        if other == 0:
            raise ZeroDivisionError("Matrix can't be divided by 0 value.")

        return self * (1 / other)

    @classmethod
    def is_valid_matrix(cls, matrix: tuple):
        if any(type(row) is not tuple for row in matrix):
            raise TypeError("All rows should be tuples")

        if any(any(type(item) is not int and type(item) is not float for item in row) for row in matrix):
            raise TypeError("Cells should be numbers")

        if any(len(matrix) != len(row) for row in matrix):
            raise ValueError("Number of rows and columns should be the same")

    @classmethod
    def unity(cls, number: int = 0):
        if type(number) is not int:
            raise TypeError("Argument should be of int type.")

        if number < 0:
            raise ValueError("Argument should be of positive value.")

        return cls(tuple(tuple(1 if i == j else 0 for i in range(number)) for j in range(number)))

    @classmethod
    def ones(cls, number: int = 0):
        if type(number) is not int:
            raise TypeError("Argument should be of int type.")

        if number < 0:
            raise ValueError("Argument should be of positive value.")

        return cls(tuple((tuple((1,) * number),) * number))


# Temporery testing section:

# a = Matrix(((1, 1, 1), (2, 2, 2), (3, 3, 3)))
# b = Matrix(((4, 4, 4), (5, 5, 5), (6, 6, 6)))
# c = Matrix(((1, 1, 1), (2, 3, 1), (0, 2, 0)))

# print(a)
# print(repr(a))
# a.tuples

# print(Matrix.unity(3))
# print(Matrix.ones(3))

# print(a + b)
# print(a + c)
# print(b + a)
# print(c + a)
# print(a + a)
# print(a + Matrix.unity(3))
# # print(a + ((1,),))

# print(a - b)
# print(b - a)
# print(a - c)
# print(c - a)
# print(a - a)
# print(a - Matrix.unity(3))
# # print(a - ((1,),))

# print(10 * a)
# print(10.1 * a)
# print(a * 10)
# print(a * 10.1)
# print(a / 10)
# print(a / 10.1)

# a = Matrix(((1, 2), (3, 4)))
# b = Matrix(((3, 5), (6, 8)))

# print(a * b)
# print(b * a)
# print(a * a)

# print(a == b)
# print(a != b)
# print(a == a)
# print(a != a)
# print(a == 1)
# print(a != 1)

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