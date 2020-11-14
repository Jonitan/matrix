import pytest

from matrix.matrix import Matrix


@pytest.fixture
def matrix_factory(request):
    assert Matrix(request.param).matrix == request.param


@pytest.fixture
def matrix_type_error_factory(request):
    with pytest.raises(TypeError):
        return Matrix(request.param)


@pytest.fixture
def matrix_value_error_factory(request):
    with pytest.raises(ValueError):
        return Matrix(request.param)


@pytest.mark.parametrize('matrix_factory', [(), ((1,),), ((1, 2), (3, 4))], indirect=True)
def test_matrix_legal_argument(matrix_factory):
    assert True


@pytest.mark.parametrize('matrix_type_error_factory', [None, 1, (1,), (('a',),)], indirect=True)
def test_matrix_wrong_type_argument(matrix_type_error_factory):
    assert True


@pytest.mark.parametrize('matrix_value_error_factory', [((1,), (1,))], indirect=True)
def test_matrix_wrong_value_argument(matrix_value_error_factory):
    assert True

