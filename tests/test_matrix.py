import pytest

from matrix.matrix import Matrix

CONSTANT_NUMBER_LIST = [50, -2.5, 0, 2]
LEGAL_MATRIX_LIST = [(()), ((1,),), ((1, 2), (-3, -4)), ((1, 2.5, 3), (3, 4, 5), (1, -5.5, 6))]
ILLEGAL_TYPE_MATRIX_LIST = [None, 1, "test", [(1,)]]
ILLEGAL_TYPE_MATRIX_CELL = [(("1",),), ((1, 1), (1, [2])), ((1, 1), (1, "[2]"))]
ILLEGAL_VALUE_MATRIX_LIST = [((), (1,)), ((1,), (1,)), ((1, 2), (1,))]
VERY_BIG_MATRIX = (((1, ) * 100), ) * 100


@pytest.fixture
def matrix_factory():
    def _matrix_factory(matrix):
        return Matrix(matrix)

    return _matrix_factory


@pytest.fixture
def compare_matrix_rows():
    def _compare_matrix_rows(matrix_a, matrix_b):
        for row_a, row_b in zip(matrix_a, matrix_b):
            assert row_a == row_b

    return _compare_matrix_rows


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_exception',
                         list(zip(LEGAL_MATRIX_LIST, [None] * len(LEGAL_MATRIX_LIST))) +
                         list(zip(ILLEGAL_TYPE_MATRIX_LIST, [TypeError] * len(ILLEGAL_TYPE_MATRIX_LIST))) +
                         list(zip(ILLEGAL_TYPE_MATRIX_CELL, [TypeError] * len(ILLEGAL_TYPE_MATRIX_CELL))) +
                         list(zip(ILLEGAL_VALUE_MATRIX_LIST, [ValueError] * len(ILLEGAL_VALUE_MATRIX_LIST))))
def test_matrix(matrix_factory, expected_matrix, expected_exception):
    if expected_exception is None:
        assert matrix_factory(expected_matrix).matrix == expected_matrix
    else:
        with pytest.raises(expected_exception):
            matrix_factory(expected_matrix)


########################################################################################################################
@pytest.mark.parametrize("test_input, expected_exception",
                         list(zip(LEGAL_MATRIX_LIST, [None] * len(LEGAL_MATRIX_LIST))) +
                         list(zip(ILLEGAL_TYPE_MATRIX_LIST, [TypeError] * len(ILLEGAL_TYPE_MATRIX_LIST))) +
                         list(zip(ILLEGAL_TYPE_MATRIX_CELL, [TypeError] * len(ILLEGAL_TYPE_MATRIX_CELL))) +
                         list(zip(ILLEGAL_VALUE_MATRIX_LIST, [ValueError] * len(ILLEGAL_VALUE_MATRIX_LIST))))
def test_is_valid_matrix(test_input, expected_exception):
    if expected_exception is None:
        Matrix.is_valid_matrix(test_input)
    else:
        with pytest.raises(expected_exception):
            Matrix.is_valid_matrix(test_input)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_tuples(matrix_factory, expected_matrix):
    assert matrix_factory(expected_matrix).tuples == expected_matrix


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_str(matrix_factory, expected_matrix):
    assert str(matrix_factory(expected_matrix)) == f"{expected_matrix}"


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_repr(matrix_factory, expected_matrix):
    assert repr(matrix_factory(expected_matrix)) == f"Matrix({expected_matrix})"


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_len(matrix_factory, expected_matrix):
    assert len(matrix_factory(expected_matrix)) == len(expected_matrix)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_getitem(compare_matrix_rows, matrix_factory, expected_matrix):
    compare_matrix_rows(matrix_factory(expected_matrix), expected_matrix)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_hash(matrix_factory, expected_matrix):
    assert hash(matrix_factory(expected_matrix)) == hash(expected_matrix)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_result', zip(
    LEGAL_MATRIX_LIST,
    [(()), ((-1,),), ((-1, -2), (3, 4)), ((-1, -2.5, -3), (-3, -4, -5), (-1, 5.5, -6))])
)
def test_matrix_neg(matrix_factory, expected_matrix, expected_result):
    assert (-matrix_factory(expected_matrix)).matrix == expected_result


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_eq(matrix_factory, expected_matrix):
    tested_matrix = matrix_factory(expected_matrix)

    assert tested_matrix == matrix_factory(expected_matrix)
    assert (tested_matrix == matrix_factory(((42, -42), (0.5, 42)))) is False

    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            tested_matrix == item


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_ne(matrix_factory, expected_matrix):
    tested_matrix = matrix_factory(expected_matrix)

    assert tested_matrix != matrix_factory(((42, -42), (0.5, 42)))
    assert (tested_matrix != matrix_factory(expected_matrix)) is False
    assert (tested_matrix != tested_matrix) is False

    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            tested_matrix != item


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_matrix', zip(
    LEGAL_MATRIX_LIST,
    [(()), ((6,),), ((-1, 7), (2, 2)), ((1, 2, 3), (3, 4, 5), (-1, -5, 16))],
    [(()), ((7,),), ((0, 9), (-1, -2)), ((2, 4.5, 6), (6, 8, 10), (0, -10.5, 22))])
)
def test_matrix_add(matrix_factory, first_matrix, second_matrix, expected_matrix):
    tested_matrix = matrix_factory(first_matrix)

    assert (tested_matrix + matrix_factory(second_matrix)).matrix == expected_matrix
    if first_matrix != (()):
        assert ((tested_matrix + tested_matrix).matrix == expected_matrix) is False

    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            tested_matrix + item

    with pytest.raises(ValueError):
        tested_matrix + matrix_factory(VERY_BIG_MATRIX)


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_matrix', zip(
    LEGAL_MATRIX_LIST,
    [(()), ((6,),), ((-1, 7), (2, 2)), ((1, 2, 3), (3, 4, 5), (-1, -5, 16))],
    [(()), ((-5,),), ((2, -5), (-5, -6)), ((0, 0.5, 0), (0, 0, 0), (2, -0.5, -10))])
)
def test_matrix_sub(matrix_factory, first_matrix, second_matrix, expected_matrix):
    tested_matrix = matrix_factory(first_matrix)

    assert (tested_matrix - matrix_factory(second_matrix)).matrix == expected_matrix
    if first_matrix != (()):
        assert ((tested_matrix - tested_matrix).matrix == expected_matrix) is False

    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            tested_matrix - item

    with pytest.raises(ValueError):
        tested_matrix - matrix_factory(VERY_BIG_MATRIX)


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_matrix, constant, expected_matrix_constant', zip(
    LEGAL_MATRIX_LIST,
    [(()), ((6,),), ((-1, 7), (2, 2)), ((1, 2, 3), (3, 4, 5), (-1, -5, 16))],
    [(()), ((6,),), ((3, 11), (-5, -29)), ((5.5, -3, 63.5), (10, -3, 109), (-21.5, -50, 71.5))],
    CONSTANT_NUMBER_LIST,
    [(()), ((-2.5,),), ((0, 0), (0, 0)), ((2, 5, 6), (6, 8, 10), (2, -11, 12))])
)
def test_matrix_mul(matrix_factory, first_matrix, second_matrix, expected_matrix, constant, expected_matrix_constant):
    tested_matrix = matrix_factory(first_matrix)

    assert (tested_matrix * constant).matrix == expected_matrix_constant
    assert (tested_matrix * matrix_factory(second_matrix)).matrix == expected_matrix
    if first_matrix != (()):
        assert ((tested_matrix * tested_matrix).matrix == expected_matrix) is False

    for item in ILLEGAL_TYPE_MATRIX_LIST:
        if type(item) is not int and type(item) is not float:
            with pytest.raises(TypeError):
                tested_matrix * item

    with pytest.raises(ValueError):
        tested_matrix * matrix_factory(VERY_BIG_MATRIX)


########################################################################################################################
@pytest.mark.parametrize('first_matrix, constant, expected_matrix_constant', zip(
    LEGAL_MATRIX_LIST,
    CONSTANT_NUMBER_LIST,
    [(()), ((-2.5,),), ((0, 0), (0, 0)), ((2, 5, 6), (6, 8, 10), (2, -11, 12))])
)
def test_matrix_rmul(matrix_factory, first_matrix, constant, expected_matrix_constant):
    tested_matrix = matrix_factory(first_matrix)

    assert (tested_matrix * constant).matrix == expected_matrix_constant

    for item in ILLEGAL_TYPE_MATRIX_LIST:
        if type(item) is not int and type(item) is not float:
            with pytest.raises(TypeError):
                item * tested_matrix


########################################################################################################################
@pytest.mark.parametrize('first_matrix, constant, expected_matrix_constant', zip(
    LEGAL_MATRIX_LIST,
    [-2.33, 0.25, 10, -1],
    [(()), ((4,),), ((0.1, 0.2), (-0.3, -0.4)), ((-1, -2.5, -3), (-3, -4, -5), (-1, 5.5, -6))])
)
def test_matrix_truediv(matrix_factory, first_matrix, constant, expected_matrix_constant):
    tested_matrix = matrix_factory(first_matrix)

    assert (tested_matrix / constant).matrix == expected_matrix_constant

    with pytest.raises(ZeroDivisionError):
        tested_matrix / 0

    for item in ILLEGAL_TYPE_MATRIX_LIST:
        if type(item) is not int and type(item) is not float:
            with pytest.raises(TypeError):
                tested_matrix / item


########################################################################################################################
@pytest.mark.parametrize("test_input, expected_exception, expected_matrix", [
    (None, TypeError, None),
    ("test", TypeError, None),
    (((1,),), TypeError, None),
    (1.1, TypeError, None),
    (-1, ValueError, None),
    (0, None, ()),
    (1, None, ((1,),)),
    (2, None, ((1, 0), (0, 1))),
    (3, None, ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
])
def test_unity(compare_matrix_rows, test_input, expected_exception, expected_matrix):
    if expected_exception is None:
        compare_matrix_rows(Matrix.unity(test_input), expected_matrix)
    else:
        with pytest.raises(expected_exception):
            Matrix.unity(test_input)


########################################################################################################################
@pytest.mark.parametrize("test_input, expected_exception, expected_matrix", [
    (None, TypeError, None),
    ("test", TypeError, None),
    (((1,),), TypeError, None),
    (1.1, TypeError, None),
    (-1, ValueError, None),
    (0, None, ()),
    (1, None, ((1,),)),
    (2, None, ((1, 1), (1, 1))),
    (3, None, ((1, 1, 1), (1, 1, 1), (1, 1, 1)))
])
def test_ones(compare_matrix_rows, test_input, expected_exception, expected_matrix):
    if expected_exception is None:
        compare_matrix_rows(Matrix.ones(test_input), expected_matrix)
    else:
        with pytest.raises(expected_exception):
            Matrix.ones(test_input)
