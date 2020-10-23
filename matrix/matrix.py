from dataclasses import dataclass


# TODO:
#   Move checks in __init__ to seperate function.
#   Add new exception types and use in a more elegant way.
#   Continue to next api required.


@dataclass(frozen=True)
class Matrix():

    matrix: tuple = ()

    def __post_init__(self):
        for row in self.matrix:
            if type(row) is not tuple:
                raise(BaseException(
                    "Row not represented by a tuple!"))
            for number in row:
                if type(number) is not int:
                    raise(BaseException(
                        "Row item not represented by a number!"))
            if len(row) != len(self.matrix):
                raise(BaseException(
                    "Number of rows different from number of columns!"))
        object.__setattr__(self, "matrix", self.matrix)

    def __str__(self):
        return "%s" % (self.matrix,)

    def __repr__(self):
        return "Matrix(%s)" % (self.matrix,)


# Temporery testing section.
a = Matrix(((1, 3), (2, 2)))
print(a.__str__())
print(a.__repr__())
