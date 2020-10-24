class RowTypeNotTuple(Exception):

    def __init__(self, row):
        self.row = row
        super().__init__()

    def __str__(self):
        return "Row represented by %s is not of Tuple type." % (self.row)


class RowItemNotNumber(Exception):

    def __init__(self, item):
        self.item = item
        super().__init__()

    def __str__(self):
        return "Item represented by %s is not of any Number type." % (self.row)


class RowAndColumnNumberDifferent(Exception):

    def __init__(self, row, row_number):
        self.row = row
        self.row_number = row_number
        self.column_number = len(row)
        super().__init__()

    def __str__(self):
        return "Rows number %s is different from columns number %s in row %s" \
            % (self.row_number, self.column_number, self.row)