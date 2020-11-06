class ObjectTypeNotMatrix(Exception):

    def __init__(self, matrix):
        self.matrix = matrix
        super().__init__()

    def __str__(self):
        return "Object represented by %s is not of Matrix type." % str(self.matrix)


class RowTypeNotTuple(Exception):

    def __init__(self, row):
        self.row = row
        super().__init__()

    def __str__(self):
        return "Row represented by %s is not of Tuple type." % str(self.row)


class RowItemNotNumber(Exception):

    def __init__(self, item):
        self.item = item
        super().__init__()

    def __str__(self):
        return "Item represented by %s is not of any Number type." % str(self.row)


class RowAndColumnNumberDifferent(Exception):

    def __init__(self, row, row_number):
        self.row = row
        self.row_number = row_number
        self.column_number = len(row)
        super().__init__()

    def __str__(self):
        return "Rows number %s is different from columns number %s in row %s" \
            % str(self.row_number), str(self.column_number), str(self.row)


class ObjectTypeNotLegalToMultiply(Exception):

    def __init__(self, item):
        self.item = item
        super().__init__()

    def __str__(self):
        return "Object represented by %s is not of legal type for matrix multiplication." % str(self.item)


class MatrixNotLegalToMultiply(Exception):

    def __init__(self, matrix):
        self.matrix = matrix
        super().__init__()

    def __str__(self):
        return "Matrix represented by %s is not of legal size for matrix multiplication." % str(self.matrix)

class IllegalInput(Exception):

    def __init__(self, item):
        self.item = item
        super().__init__()

    def __str__(self):
        return "Illigal input %s to requested operation." % str(self.item)
