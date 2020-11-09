from dataclasses import dataclass

from matrix_exceptions import RowTypeNotTuple, RowItemNotNumber, RowAndColumnNumberDifferent, ObjectTypeNotMatrix, \
                              ObjectTypeNotLegalToMultiply, MatrixNotLegalToMultiply, IllegalInput

# TODO:
#   Add documentation.

@dataclass(frozen=True)
class Matrix:

    matrix: tuple = ()

    def __post_init__(self):
        if self.is_valid_matrix():
            object.__setattr__(self, "matrix", self.matrix)
            object.__setattr__(self, "order", len(self.matrix))
            object.__setattr__(self, "row_pointer", 0)

    def __str__(self):
        return "%s" % (self.matrix,)

    def __repr__(self):
        return "Matrix(%s)" % (self.matrix,)

    def __neg__(self):
        return Matrix(tuple(tuple(-item for item in self.matrix[j]) for j in range(self.order)))

    def __add__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        if self.order >= other.order:
            return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                      if i < other.order and j < other.order else self.matrix[j][i]
                                      for i in range(self.order)) for j in range(self.order)))
        else:
            return Matrix(tuple(tuple(self.matrix[j][i] + other.matrix[j][i]
                                      if i < self.order and j < self.order else other.matrix[j][i]
                                      for i in (range(other.order))) for j in (range(other.order))))

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Matrix(tuple(tuple(self.matrix[j][i] * other
                                      for i in range(self.order)) for j in range(self.order)))

        elif type(other) is Matrix:
            if self.order != other.order:
                raise MatrixNotLegalToMultiply(other)

            return Matrix(tuple(tuple(sum(row[i] * cul[i] for i in range(self.order)) for cul in zip(*other))
                                for row in self))
        else:
            raise ObjectTypeNotLegalToMultiply(other)

    def __rmul__(self, other):
        if type(other) is not int and type(other) is not float:
            raise ObjectTypeNotLegalToMultiply(other)

        return Matrix(tuple(tuple(self.matrix[j][i] * other
                                  for i in range(self.order)) for j in range(self.order)))

    def __sub__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        return self + (-other)

    def __truediv__(self, other):
        if type(other) is not int and type(other) is not float:
            raise ObjectTypeNotLegalToMultiply(other)

        return Matrix(tuple(tuple(self.matrix[j][i] / other
                                  for i in range(self.order)) for j in range(self.order)))

    def __eq__(self, other):
        if type(other) is not Matrix:
            raise ObjectTypeNotMatrix(other)

        if self.order != other.order:
            return False

        for i in range(self.order):
            if self.matrix[i] != other.matrix[i]:
                return False

        return True

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        object.__setattr__(self, "row_pointer", 0)
        return self

    def __next__(self):
        if self.row_pointer >= self.order:
            raise StopIteration
        else:
            result = self.matrix[self.row_pointer]
            object.__setattr__(self, "row_pointer", self.row_pointer + 1)
            return result

    def __hash__(self):
        return hash((tuple(self.matrix[j][i] for i in range(self.order) for j in range(self.order)), self.order))

    @property
    def tuples(self):
        print("%s" % (self.matrix,))

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
a = Matrix(((1, 1), (2, 3)))
b = Matrix(((1,),))
c = Matrix(((1, 1, 1), (2, 3, 1), (0, 2, 0)))

print(a)

print(repr(a))

a.tuples

print(Matrix.unity(3))

print(Matrix.ones(2))

print(a + b)
print(a + c)
print(b + a)
print(c + a)
print(a + a)
print(a + Matrix.unity(2))
# print(a + ((1,),))

print(a - b)
print(b - a)
print(a - c)
print(c - a)
print(a - a)
print(a - Matrix.unity(2))
# print(a - ((1,),))

print(10 * a)
print(10.1 * a)
print(a / 10)
print(a / 10.1)

b = Matrix(((2, 2), (1, 1)))

print(a * b)
print(b * a)

print(a == b)
print(a != b)

b = Matrix(((1, 1), (2, 3)))

print(a == b)
print(a != b)

for i in a:
    print(str(i))

dictionary = {}
dictionary[Matrix(((1, 1), (2, 2)))] = 1
dictionary[Matrix(((1, 1), (2, 2)))] = 2
dictionary[Matrix(((1, 1), (2, 3)))] = 3
print(dictionary)