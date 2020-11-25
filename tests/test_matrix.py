import pytest

from matrix.matrix import Matrix


LEGAL_MATRIX_LIST = [(()), ((1,),), ((1, 2), (3, 4)), ((1, 2, 3), (3, 4, 5), (1, 5, 6))]
ILLEGAL_TYPE_MATRIX_LIST = [None, 1, "test", [(1,)]]
ILLEGAL_VALUE_MATRIX_LIST = [((), (1,)), ((), (1,)), ((1,), (1,)), ((1, 2), (1,))]
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
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_legal_argument(matrix_factory, expected_matrix):
    assert matrix_factory(expected_matrix).matrix == expected_matrix


@pytest.mark.parametrize('expected_matrix', ILLEGAL_TYPE_MATRIX_LIST)
def test_matrix_type_error(matrix_factory, expected_matrix):
    with pytest.raises(TypeError):
        matrix_factory(expected_matrix)


@pytest.mark.parametrize('expected_matrix', [((), (1,)), ((1,), (1,)), ((1, 2), (1,))])
def test_matrix_value_error(matrix_factory, expected_matrix):
    with pytest.raises(ValueError):
        matrix_factory(expected_matrix)


########################################################################################################################
@pytest.mark.parametrize("test_input, expected_exception", [
    (None, TypeError),
    (1, TypeError),
    ((1,), TypeError),
    (((1,), (1,)), ValueError),
    ((), None),
    (((1,),), None),
    (((1, 2), (4, 5)), None)
])
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
@pytest.mark.parametrize('expected_matrix', [(()), ((1,),), ((1, 2), (3, 4)), ((1, 2, 3), (3, 4, 5), (1, 5, 6))])
def test_matrix_hash(matrix_factory, expected_matrix):
    assert hash(matrix_factory(expected_matrix)) == hash(item for item in expected_matrix)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_neg(matrix_factory, expected_matrix):
    assert (-matrix_factory(expected_matrix)).matrix == tuple(tuple(-item for item in row) for row in expected_matrix)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_eq(matrix_factory, expected_matrix):
    assert matrix_factory(expected_matrix) == matrix_factory(expected_matrix)
    assert (matrix_factory(expected_matrix) == matrix_factory(((42, -42), (0, 42)))) is False
    matrix = matrix_factory(expected_matrix)
    assert matrix == matrix
    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            matrix_factory(expected_matrix) == item


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', LEGAL_MATRIX_LIST)
def test_matrix_ne(matrix_factory, expected_matrix):
    assert matrix_factory(expected_matrix) != matrix_factory(((42, -42), (0, 42)))
    assert (matrix_factory(expected_matrix) != matrix_factory(expected_matrix)) is False
    matrix = matrix_factory(expected_matrix)
    assert (matrix != matrix) is False
    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            matrix_factory(expected_matrix) != item


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_matrix',
                         zip(LEGAL_MATRIX_LIST,
                             [(()), ((6,),), ((-1, 7), (2, 2)), ((1, 2, 3), (3, 4, 5), (-1, -5, 16))],
                             [(()), ((7,),), ((0, 9), (5, 6)), ((2, 4, 6), (6, 8, 10), (0, 0, 22))])
                         )
def test_matrix_add(matrix_factory, first_matrix, second_matrix, expected_matrix):
    assert (matrix_factory(first_matrix) + matrix_factory(second_matrix)).matrix == expected_matrix
    if first_matrix != (()):
        assert ((matrix_factory(first_matrix) + matrix_factory(expected_matrix)).matrix == second_matrix) is False
    matrix = matrix_factory(first_matrix)
    assert (matrix + matrix).matrix == tuple(tuple(cell * 2 for cell in row) for row in first_matrix)
    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            matrix_factory(first_matrix) + item
        with pytest.raises(ValueError):
            matrix_factory(first_matrix) + matrix_factory(VERY_BIG_MATRIX)


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_matrix',
                         zip(LEGAL_MATRIX_LIST,
                             [(()), ((6,),), ((-1, 7), (2, 2)), ((1, 2, 3), (3, 4, 5), (-1, -5, 16))],
                             [(()), ((-5,),), ((2, -5), (1, 2)), ((0, 0, 0), (0, 0, 0), (2, 10, -10))])
                         )
def test_matrix_sub(matrix_factory, first_matrix, second_matrix, expected_matrix):
    assert (matrix_factory(first_matrix) - matrix_factory(second_matrix)).matrix == expected_matrix
    if first_matrix != (()):
        assert ((matrix_factory(second_matrix) - matrix_factory(first_matrix)).matrix == expected_matrix) is False
    matrix = matrix_factory(first_matrix)
    assert (matrix - matrix).matrix == tuple((tuple((0,) * len(matrix)),) * len(matrix))
    for item in ILLEGAL_TYPE_MATRIX_LIST:
        with pytest.raises(TypeError):
            matrix_factory(first_matrix) - item
        with pytest.raises(ValueError):
            matrix_factory(first_matrix) - matrix_factory(VERY_BIG_MATRIX)


########################################################################################################################
@pytest.mark.parametrize("test_input, expected_exception, expected_matrix", [
    (None, TypeError, None),
    (-1, ValueError, None),
    ("test", TypeError, None),
    (((1,),), TypeError, None),
    (1.1, TypeError, None),
    (0, None, ()),
    (1, None, ((1,),)),
    (2, None, ((1, 0), (0, 1))),
    (20, None, tuple(tuple(1 if i == j else 0 for i in range(20)) for j in range(20)))
])
def test_unity(compare_matrix_rows, test_input, expected_exception, expected_matrix):
    if expected_exception is None and expected_matrix is not None:
        compare_matrix_rows(Matrix.unity(test_input), expected_matrix)
    else:
        with pytest.raises(expected_exception):
            Matrix.unity(test_input)


########################################################################################################################
@pytest.mark.parametrize("test_input, expected_exception, expected_matrix", [
    (None, TypeError, None),
    (-1, ValueError, None),
    ("test", TypeError, None),
    (((1,),), TypeError, None),
    (1.1, TypeError, None),
    (0, None, ()),
    (1, None, ((1,),)),
    (20, None, (((1,) * 20),) * 20),
])
def test_ones(compare_matrix_rows, test_input, expected_exception, expected_matrix):
    if expected_exception is None and expected_matrix is not None:
        compare_matrix_rows(Matrix.ones(test_input), expected_matrix)
    else:
        with pytest.raises(expected_exception):
            Matrix.ones(test_input)
