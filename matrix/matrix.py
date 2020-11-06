from dataclasses import dataclass
from typing import ClassVar

from matrix_exceptions import RowTypeNotTuple, RowItemNotNumber, RowAndColumnNumberDifferent, ObjectTypeNotMatrix, \
                              ObjectTypeNotLegalToMultiply, MatrixNotLegalToMultiply, IllegalInput

# TODO:
#   Add comparison, iteration & hash.


def calc_mul_single_cell(row: tuple = None, cul: tuple = None):
    if row is None or cul is None:
        return None

    if len(row) != len(cul):
        return None

    result = 0
    for i in range(len(row)):
        result = result + (row[i] * cul[i])

    return result


@dataclass(frozen=True)
class Matrix:

    # ((1,1),(2,3)) -> 2 rows, 2 culomns:
    # Column 1: (1,1) Column 2: (2,3)
    # Row 1: (1,2) Row 2: (1,3)

    matrix: tuple = ()

    def __post_init__(self):
        if self.is_valid_matrix():
            object.__setattr__(self, "matrix", self.matrix)
            object.__setattr__(self, "rows_number", len(self.matrix))

    def __str__(self):
        return "%s" % (self.matrix,)

    def __repr__(self):
        return "Matrix(%s)" % (self.matrix,)

    def __add__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        rows_num_b = len(other.matrix)
        if self.rows_number >= rows_num_b:
            return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                      if i < rows_num_b and j < rows_num_b else self.matrix[j][i]
                                      for i in (range(self.rows_number))) for j in (range(self.rows_number))))
        else:
            return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                      if i < self.rows_number and j < self.rows_number else other.matrix[j][i]
                                      for i in (range(rows_num_b))) for j in (range(rows_num_b))))

    def __sub__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        rows_num_b = len(other.matrix)
        if self.rows_number >= rows_num_b:
            return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                                      if i < rows_num_b and j < rows_num_b
                                      else self.matrix[j][i]
                                      for i in (range(self.rows_number))) for j in (range(self.rows_number))))
        else:
            return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                                      if i < self.rows_number and j < self.rows_number else -other.matrix[j][i]
                                      for i in (range(rows_num_b))) for j in (range(rows_num_b))))

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Matrix(tuple(tuple(self.matrix[j][i] * other
                                      for i in range(self.rows_number)) for j in range(self.rows_number)))

        elif type(other) is Matrix:
            if len(self.matrix[0]) != other.rows_number:
                raise MatrixNotLegalToMultiply(other)

            columns_cum_b = len(other.matrix[0])
            return Matrix(tuple(tuple(calc_mul_single_cell(self.get_row_as_tuple(j), other.matrix[i])
                                      for i in range(columns_cum_b)) for j in range(self.rows_number)))
        else:
            raise ObjectTypeNotLegalToMultiply(other)
        return

    def __rmul__(self, other):
        if type(other) is not int and type(other) is not float:
            raise ObjectTypeNotLegalToMultiply(other)

        return Matrix(tuple(tuple(self.matrix[j][i] * other
                                  for i in (range(self.rows_number))) for j in (range(self.rows_number))))

    def __truediv__(self, other):
        if type(other) is not int and type(other) is not float:
            raise ObjectTypeNotLegalToMultiply(other)

        return Matrix(tuple(tuple(self.matrix[j][i] / other
                                  for i in (range(self.rows_number))) for j in (range(self.rows_number))))

    @property
    def tuples(self):
        print("%s" % (self.matrix,))

    def get_row_as_tuple(self, row_number: int = None):
        if row_number is None or row_number < 0 or self.rows_number < row_number:
            return None

        return tuple(self.matrix[i][row_number] for i in range(self.rows_number))

    @classmethod
    def unity(cls, number: int = 0):
        if type(number) is not int or number < 0:
            raise IllegalInput(number)

        return cls(tuple(tuple(1 if i == j else 0 for i in range(number)) for j in range(number)))

    @classmethod
    def ones(cls, number):
        if type(number) is not int or number < 0:
            raise IllegalInput(number)

        return cls(tuple(tuple(1 for i in range(number)) for i in range(number)))

    def is_valid_matrix(self):
        for row in self.matrix:
            if type(row) is not tuple:
                raise RowTypeNotTuple(row)
            for item in row:
                if type(item) is not int and type(item) is not float:
                    raise RowItemNotNumber(item)
            if len(row) != len(self.matrix):
                raise RowAndColumnNumberDifferent(row, len(self.matrix))
        return True


# Temporery testing section:

a = Matrix(((1, 1), (2, 3)))
b = Matrix(((1,),))
c = Matrix(((1, 1, 1), (2, 3, 1), (0, 2, 0)))

# print(a)
#
# print(repr(a))
#
# a.tuples
#
# print(Matrix.unity(3))
#
# print(Matrix.ones(2))

# print(a + b)
# print(a + c)
# print(a + a)
# print(a + Matrix.unity(2))
# print(a + ((1,),))

# print(a - b)
# print(a - c)
# print(c - a)
# print(a - a)
# print(a - Matrix.unity(2))
# print(a - ((1,),))

# print(10 * a)
# print(10.1 * a)
# print(a / 10)
# print(a / 10.1)

# b = Matrix(((2, 2), (1, 1)))
#
# print(a * b)
# print(b * a)