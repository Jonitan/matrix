from dataclasses import dataclass

from matrix_exceptions import \
    RowTypeNotTuple, RowItemNotNumber, RowAndColumnNumberDifferent

# TODO:
#   Finish current TODO's.
#   Add new exceptions types.
#   Add comparison, iteration & hash.


@dataclass(frozen=True)
class Matrix():

    matrix: tuple = ()

    def __post_init__(self):
        if self.is_valid_matrix():
            object.__setattr__(self, "matrix", self.matrix)

    def __str__(self):
        return "%s" % (self.matrix,)

    def __repr__(self):
        return "Matrix(%s)" % (self.matrix,)

    def __add__(self, other):
        if type(other) is not Matrix:
            raise "..."
        rows_num_a = len(self.matrix)
        rows_num_b = len(other.matrix)
        if rows_num_a >= rows_num_b:
            return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                if i < rows_num_b and j < rows_num_b else self.matrix[j][i]
                for i in (range(rows_num_a))) for j in (range(rows_num_a))))
        else:
            return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                if i < rows_num_a and j < rows_num_a else other.matrix[j][i]
                for i in (range(rows_num_b))) for j in (range(rows_num_b))))

    def __sub__(self, other):
        if type(other) is not Matrix:
            raise "..."
        rows_num_a = len(self.matrix)
        rows_num_b = len(other.matrix)
        if rows_num_a >= rows_num_b:
            return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                if i < rows_num_b and j < rows_num_b else self.matrix[j][i]
                for i in (range(rows_num_a))) for j in (range(rows_num_a))))
        else:
            return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                if i < rows_num_a and j < rows_num_a else -other.matrix[j][i]
                for i in (range(rows_num_b))) for j in (range(rows_num_b))))

    def __mul__(self, other):
        if type(other) is int or float:
            rows_num_a = len(self.matrix)
            return Matrix(tuple(tuple(self.matrix[j][i] * other
                for i in (range(rows_num_a))) for j in (range(rows_num_a))))
        elif type(other) is Matrix:
            # TODO
            raise "Not Implemented!"
        else:
            # TODO
            raise "Not Implemented!"
        return

    def __rmul__(self, other):
        if type(other) is not int and not float:
            # TODO
            raise "Not Implemented!"

        rows_num_a = len(self.matrix)
        return Matrix(tuple(tuple(self.matrix[j][i] * other
            for i in (range(rows_num_a))) for j in (range(rows_num_a))))

    def __truediv__(self, other):
        if type(other) is not int and not float:
            # TODO
            raise "Not Implemented!"

        rows_num_a = len(self.matrix)
        return Matrix(tuple(tuple(self.matrix[j][i] / other
            for i in (range(rows_num_a))) for j in (range(rows_num_a))))

    @property
    def tuples(self):
        print("%s" % (self.matrix,))

    @classmethod
    def unity(cls, number):
        if type(number) is not int:
            # TODO
            raise "Not Implemented!"

        if number < 0:
            # TODO
            raise "Not Implemented!"

        return cls(tuple(tuple(1 if i == j else 0 for i in range(number)) for j in range(number)))

    @classmethod
    def ones(cls, number):
        if type(number) is not int:
            # TODO
            raise "Not Implemented!"

        if number < 0:
            # TODO
            raise "Not Implemented!"

        return cls(tuple(tuple(1 for i in range(number)) for j in range(number)))

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

# a = Matrix(((1, 1), (2, 3)))
# b = Matrix(((1,),))
# c = Matrix(((1, 1, 1), (2, 3, 1), (0, 2, 0)))

# print(a)

# print(a.__repr__)

# a.tuples

# print(Matrix.unity(3))

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