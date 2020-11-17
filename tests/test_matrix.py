import pytest

from matrix.matrix import Matrix


LEGAL_MATRIX_LIST = [(()), ((1,),), ((1, 2), (3, 4)), ((1, 2, 3), (3, 4, 5), (1, 5, 6))]
ILLEGAL_TYPE_MATRIX_LIST = [None, 1, "test", [(1,)]]
ILLEGAL_VALUE_MATRIX_LIST = [((), (1,)), ((), (1,)), ((1,), (1,)), ((1, 2), (1,))]


@pytest.fixture
def matrix_factory():
    def _matrix_factory(matrix):
        return Matrix(matrix)

    return _matrix_factory


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
@pytest.mark.parametrize("test_input,expected_exception", [
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
        assert True
    else:
        with pytest.raises(expected_exception):
            assert Matrix.is_valid_matrix(test_input)


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
def test_matrix_getitem(matrix_factory, expected_matrix):
    # TODO
    pass


########################################################################################################################
@pytest.mark.parametrize('expected_matrix', [(()), ((1,),), ((1, 2), (3, 4)), ((1, 2, 3), (3, 4, 5), (1, 5, 6))])
def test_matrix_hash(matrix_factory, expected_matrix):
    assert hash(matrix_factory(expected_matrix)) == hash(item for item in expected_matrix)



