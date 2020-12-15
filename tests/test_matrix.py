import pytest

from matrix.matrix import Matrix


@pytest.fixture
def compare_matrix_rows():
    def _compare_matrix_rows(matrix_a, matrix_b):
        for row_a, row_b in zip(matrix_a, matrix_b):
            assert row_a == row_b

    return _compare_matrix_rows


########################################################################################################################
@pytest.mark.parametrize('matrix_input, expected_exception', [
    ((()), None),
    (((1,),), None),
    (((1, 2.5), (-3, -4)), None),
    (None, TypeError),
    (1, TypeError),
    ((("1",),), TypeError),
    (((), (1,)), ValueError)
])
def test_matrix_initialization(matrix_input, expected_exception):
    if expected_exception is None:
        assert Matrix(matrix_input).matrix == matrix_input
    else:
        with pytest.raises(expected_exception):
            Matrix(matrix_input)


########################################################################################################################
@pytest.mark.parametrize("test_input, expected_exception", [
    ((()), None),
    (((1,),), None),
    (((1, 2.5), (-3, -4)), None),
    (None, TypeError),
    (1, TypeError),
    ((("1",),), TypeError),
    (((), (1,)), ValueError)
])
def test_is_valid_matrix(test_input, expected_exception):
    if expected_exception is None:
        Matrix.is_valid_matrix(test_input)
    else:
        with pytest.raises(expected_exception):
            Matrix.is_valid_matrix(test_input)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_tuples', [
    (Matrix((())), (())),
    (Matrix(((1,),)), ((1,),)),
    (Matrix(((1, 2.5), (-3, -4))), ((1, 2.5), (-3, -4)))
])
def test_matrix_tuples(expected_matrix, expected_tuples):
    assert expected_matrix.tuples == expected_tuples


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_str', [
    (Matrix((())), '()'),
    (Matrix(((1,),)), '((1,),)'),
    (Matrix(((1, 2.5), (-3, -4))), '((1, 2.5), (-3, -4))')
])
def test_matrix_str(expected_matrix, expected_str):
    assert str(expected_matrix) == expected_str


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_repr', [
    (Matrix((())), 'Matrix(())'),
    (Matrix(((1,),)), 'Matrix(((1,),))'),
    (Matrix(((1, 2.5), (-3, -4))), 'Matrix(((1, 2.5), (-3, -4)))')
])
def test_matrix_repr(expected_matrix, expected_repr):
    assert repr(expected_matrix) == expected_repr


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_length', [
    (Matrix((())), 0),
    (Matrix(((1,),)), 1),
    (Matrix(((1, 2.5), (-3, -4))), 2)
])
def test_matrix_len(expected_matrix, expected_length):
    assert len(expected_matrix) == expected_length


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_equal', [
    (Matrix((())), (())),
    (Matrix(((1,),)), ((1,),)),
    (Matrix(((1, 2.5), (-3, -4))), ((1, 2.5), (-3, -4)))
])
def test_matrix_getitem(compare_matrix_rows, expected_matrix, expected_equal):
    compare_matrix_rows(expected_matrix, expected_equal)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_equal', [
    (Matrix((())), (())),
    (Matrix(((1,),)), ((1,),)),
    (Matrix(((1, 2.5), (-3, -4))), ((1, 2.5), (-3, -4)))
])
def test_matrix_hash(expected_matrix, expected_equal):
    assert hash(expected_matrix) == hash(expected_equal)


########################################################################################################################
@pytest.mark.parametrize('expected_matrix, expected_result', [
    (Matrix((())), (())),
    (Matrix(((1,),)), ((-1,),)),
    (Matrix(((1, 2.5), (-3, -4))), ((-1, -2.5), (3, 4)))
])
def test_matrix_neg(expected_matrix, expected_result):
    assert (-expected_matrix).matrix == expected_result


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_result', [
    (Matrix((())), Matrix((())), True),
    (Matrix(((1,),)), Matrix(((-1,),)), False),
    (Matrix(((1,),)), Matrix(((1,),)), True),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1, 2.5), (-3, -4))), True),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1,),)), False),
    (Matrix(((1, 2.5), (-3, -4))), None, TypeError),
])
def test_matrix_eq(first_matrix, second_matrix, expected_result):
    if expected_result is TypeError:
        with pytest.raises(expected_result):
            first_matrix == second_matrix
    else:
        assert (first_matrix == second_matrix) == expected_result


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_result', [
    (Matrix((())), Matrix((())), False),
    (Matrix(((1,),)), Matrix(((-1,),)), True),
    (Matrix(((1,),)), Matrix(((1,),)), False),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1, 2.5), (-3, -4))), False),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1,),)), True),
    (Matrix(((1, 2.5), (-3, -4))), None, TypeError),
])
def test_matrix_ne(first_matrix, second_matrix, expected_result):
    if expected_result is TypeError:
        with pytest.raises(expected_result):
            first_matrix != second_matrix
    else:
        assert (first_matrix != second_matrix) == expected_result


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_result', [
    (Matrix((())), Matrix((())), Matrix((()))),
    (Matrix(((1,),)), Matrix(((-1,),)), Matrix(((0,),))),
    (Matrix(((1,),)), Matrix(((1,),)), Matrix(((2,),))),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1, 1.5), (1, 1))), Matrix(((2, 4), (-2, -3)))),
    (Matrix(((1, 2.5), (-3, -4))), None, TypeError),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1,),)), ValueError),
])
def test_matrix_add(first_matrix, second_matrix, expected_result):
    if expected_result is TypeError or expected_result is ValueError:
        with pytest.raises(expected_result):
            first_matrix + second_matrix
    else:
        assert (first_matrix + second_matrix) == expected_result


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_result', [
    (Matrix((())), Matrix((())), Matrix((()))),
    (Matrix(((1,),)), Matrix(((-1,),)), Matrix(((2,),))),
    (Matrix(((1,),)), Matrix(((1,),)), Matrix(((0,),))),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1, 1.5), (1, 1))), Matrix(((0, 1.0), (-4, -5)))),
    (Matrix(((1, 2.5), (-3, -4))), None, TypeError),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1,),)), ValueError),
])
def test_matrix_sub(first_matrix, second_matrix, expected_result):
    if expected_result is TypeError or expected_result is ValueError:
        with pytest.raises(expected_result):
            first_matrix - second_matrix
    else:
        assert (first_matrix - second_matrix) == expected_result


########################################################################################################################
@pytest.mark.parametrize('first_matrix, second_matrix, expected_result', [
    (Matrix((())), Matrix((())), Matrix((()))),
    (Matrix(((1,),)), Matrix(((5,),)), Matrix(((5,),))),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((2, -2), (0, 5.5))), Matrix(((2, 11.75), (-6, -16)))),
    (Matrix(((1, 2.5), (-3, -4))), 2, Matrix(((2, 5), (-6, -8)))),
    (Matrix(((1, 2.5), (-3, -4))), None, TypeError),
    (Matrix(((1, 2.5), (-3, -4))), Matrix(((1,),)), ValueError),
])
def test_matrix_mul(first_matrix, second_matrix, expected_result):
    if expected_result is TypeError or expected_result is ValueError:
        with pytest.raises(expected_result):
            first_matrix * second_matrix
    else:
        assert (first_matrix * second_matrix) == expected_result


# ########################################################################################################################
@pytest.mark.parametrize('first_matrix, constant, expected_result', [
    (Matrix((())), 1, Matrix((()))),
    (Matrix(((1,),)), -0.5, Matrix(((-0.5,),))),
    (Matrix(((1, 2.5), (-3, -4))), 2, Matrix(((2, 5), (-6, -8)))),
    (Matrix(((1, 2.5), (-3, -4))), None, TypeError),
])
def test_matrix_rmul(first_matrix, constant, expected_result):
    if expected_result is TypeError:
        with pytest.raises(expected_result):
            constant * first_matrix
    else:
        assert (constant * first_matrix) == expected_result


# ########################################################################################################################
@pytest.mark.parametrize('first_matrix, constant, expected_result', [
    (Matrix((())), 1, Matrix((()))),
    (Matrix(((1,),)), -0.5, Matrix(((-2,),))),
    (Matrix(((1, 2.5), (-3, -4))), 2, Matrix(((0.5, 1.25), (-1.5, -2)))),
    (Matrix(((1, 2.5), (-3, -4))), None, TypeError),
    (Matrix(((1, 2.5), (-3, -4))), 0, ZeroDivisionError),
])
def test_matrix_truediv(first_matrix, constant, expected_result):
    if expected_result is TypeError or expected_result is ZeroDivisionError:
        with pytest.raises(expected_result):
            first_matrix / constant
    else:
        assert (first_matrix / constant) == expected_result


########################################################################################################################
@pytest.mark.parametrize("input_length, expected_result", [
    (None, TypeError),
    (-1, ValueError),
    (0, Matrix((()))),
    (1, Matrix(((1,),))),
    (2, Matrix(((1, 0), (0, 1)))),
])
def test_unity(input_length, expected_result):
    if expected_result is TypeError or expected_result is ValueError:
        with pytest.raises(expected_result):
            Matrix.unity(input_length)
    else:
        assert Matrix.unity(input_length) == expected_result


########################################################################################################################
@pytest.mark.parametrize("input_length, expected_result", [
    (None, TypeError),
    (-1, ValueError),
    (0, Matrix((()))),
    (1, Matrix(((1,),))),
    (2, Matrix(((1, 1), (1, 1)))),
])
def test_ones(input_length, expected_result):
    if expected_result is TypeError or expected_result is ValueError:
        with pytest.raises(expected_result):
            Matrix.ones(input_length)
    else:
        assert Matrix.ones(input_length) == expected_result
