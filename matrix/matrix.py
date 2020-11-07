from dataclasses import dataclass

from matrix_exceptions import RowTypeNotTuple, RowItemNotNumber, RowAndColumnNumberDifferent, ObjectTypeNotMatrix, \
                              ObjectTypeNotLegalToMultiply, MatrixNotLegalToMultiply, IllegalInput

# TODO:
#   Add documentation.


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

    matrix: tuple = ()

    def __post_init__(self):
        if self.is_valid_matrix():
            object.__setattr__(self, "matrix", self.matrix)
            object.__setattr__(self, "rows_number", len(self.matrix))
            object.__setattr__(self, "culomns_number", len(self.matrix[0]))
            object.__setattr__(self, "row_pointer", 0)

    def __str__(self):
        return "%s" % (self.matrix,)

    def __repr__(self):
        return "Matrix(%s)" % (self.matrix,)

    def __add__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        if self.rows_number >= other.rows_number:
            if self.culomns_number >= other.culomns_number:
                return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                          if i < other.culomns_number and j < other.rows_number else self.matrix[j][i]
                                          for i in range(self.culomns_number)) for j in range(self.rows_number)))
            else:
                return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                          if i < self.culomns_number and j < other.rows_number else
                                          self.matrix[j][i] if i < self.culomns_number and j >= other.rows_number else
                                          other.matrix[j][i] for i in range(other.culomns_number))
                                    for j in range(self.rows_number)))
        else:
            if self.culomns_number >= other.culomns_number:
                return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                          if i < other.culomns_number and j < self.rows_number else
                                          other.matrix[j][i] if i < other.culomns_number and j >= self.rows_number else
                                          self.matrix[j][i] for i in (range(self.culomns_number)))
                                    for j in (range(other.rows_number))))
            else:
                return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                          if i < self.culomns_number and j < self.rows_number else other.matrix[j][i]
                                          for i in (range(other.culomns_number))) for j in (range(other.rows_number))))

    def __sub__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        if self.rows_number >= other.rows_number:
            if self.culomns_number >= other.culomns_number:
                return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                                          if i < other.culomns_number and j < other.rows_number else self.matrix[j][i]
                                          for i in range(self.culomns_number)) for j in range(self.rows_number)))
            else:
                return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                                          if i < self.culomns_number and j < other.rows_number else
                                          self.matrix[j][i] if i < self.culomns_number and j >= other.rows_number else
                                          -other.matrix[j][i] for i in range(other.culomns_number))
                                    for j in range(self.rows_number)))
        else:
            if self.culomns_number >= other.culomns_number:
                return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                                          if i < other.culomns_number and j < self.rows_number else
                                          -other.matrix[j][i] if i < other.culomns_number and j >= self.rows_number else
                                          self.matrix[j][i] for i in (range(self.culomns_number)))
                                    for j in (range(other.rows_number))))
            else:
                return Matrix(tuple(tuple(self.matrix[j][i] - other.matrix[j][i]
                                          if i < self.culomns_number and j < self.rows_number else -other.matrix[j][i]
                                          for i in (range(other.culomns_number))) for j in (range(other.rows_number))))

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Matrix(tuple(tuple(self.matrix[j][i] * other
                                      for i in range(self.culomns_number)) for j in range(self.rows_number)))

        elif type(other) is Matrix:
            if self.culomns_number != other.rows_number:
                raise MatrixNotLegalToMultiply(other)

            return Matrix(tuple(tuple(calc_mul_single_cell(self.matrix[j], other.get_culomn_as_tuple(i))
                                      for i in range(other.culomns_number)) for j in range(self.rows_number)))
        else:
            raise ObjectTypeNotLegalToMultiply(other)

    def __rmul__(self, other):
        if type(other) is not int and type(other) is not float:
            raise ObjectTypeNotLegalToMultiply(other)

        return Matrix(tuple(tuple(self.matrix[j][i] * other
                                  for i in range(self.culomns_number)) for j in range(self.rows_number)))

    def __truediv__(self, other):
        if type(other) is not int and type(other) is not float:
            raise ObjectTypeNotLegalToMultiply(other)

        return Matrix(tuple(tuple(self.matrix[j][i] / other
                                  for i in range(self.culomns_number)) for j in range(self.rows_number)))

    def __eq__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        if self.rows_number != other.rows_number or self.culomns_number != other.culomns_number:
            return False

        for i in range(self.rows_number):
            if self.matrix[i] != other.matrix[i]:
                return False

        return True

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        object.__setattr__(self, "row_pointer", 0)
        return self

    def __next__(self):
        if self.row_pointer >= self.rows_number:
            raise StopIteration
        else:
            result = self.matrix[self.row_pointer]
            object.__setattr__(self, "row_pointer", self.row_pointer + 1)
            return result

    def __hash__(self):
        return hash((tuple(self.matrix[j][i] for i in range(self.culomns_number) for j in range(self.rows_number)),
                     self.rows_number, self.culomns_number))

    @property
    def tuples(self):
        print("%s" % (self.matrix,))

    def get_culomn_as_tuple(self, culomn_number: int = None):
        if culomn_number is None or culomn_number < 0 or self.rows_number < culomn_number:
            return None

        return tuple(self.matrix[i][culomn_number] for i in range(self.rows_number))

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

    @classmethod
    def unity(cls, number: int = 0):
        if type(number) is not int or number < 0:
            raise IllegalInput(number)

        return cls(tuple(tuple(1 if i == j else 0 for i in range(number)) for j in range(number)))

    @classmethod
    def ones(cls, number: int = 0):
        if type(number) is not int or number < 0:
            raise IllegalInput(number)

        return cls(tuple(tuple(1 for i in range(number)) for i in range(number)))


# Temporery testing section:

# a = Matrix(((1, 1), (2, 3)))

# b = Matrix(((1,),))
# c = Matrix(((1, 1, 1), (2, 3, 1), (0, 2, 0)))
#
# a = Matrix(((1, 2), (3, 4)))
# b = Matrix(((3, 5), (6, 8)))

# print(a)

# print(repr(a))

# a.tuples

# print(Matrix.unity(3))

# print(Matrix.ones(2))

# print(a + b)
# print(a + c)
# print(b + a)
# print(c + a)
# print(a + a)
# print(a + Matrix.unity(2))
# print(a + ((1,),))

# print(a - b)
# print(b - a)
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

# print(a * b)
# print(b * a)

# print(a == b)
# print(a != b)

# b = Matrix(((1, 1), (2, 3)))

# print(a == b)
# print(a != b)

# for i in a:
#     print(str(i))

# dictionary = {}
# dictionary[Matrix(((1, 1), (2, 2)))] = 1
# dictionary[Matrix(((1, 1), (2, 2)))] = 2
# dictionary[Matrix(((1, 1), (2, 3)))] = 3
# print(dictionary)