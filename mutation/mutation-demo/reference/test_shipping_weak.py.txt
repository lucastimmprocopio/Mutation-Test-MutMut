"""
SUITE DE TESTES "FRACA" (versão do PROBLEMA)
100% de cobertura, mas só checa que "não quebra". O mutmut expõe isso.
"""

from shipping import calculate_order_total


def test_calculate_order_total_runs_without_error():
    result = calculate_order_total(100, 1)
    assert result is not None


def test_calculate_order_total_returns_a_number():
    result = calculate_order_total(100, 5, "PROMO10")
    assert isinstance(result, float)


def test_calculate_order_total_with_high_quantity():
    result = calculate_order_total(100, 10, "PROMO20")
    assert result >= 0


def test_calculate_order_total_with_zero_quantity():
    result = calculate_order_total(50, 0)
    assert result > 0


def test_calculate_order_total_with_three_items():
    result = calculate_order_total(100, 3)
    assert result > 0


def test_negative_subtotal_raises_value_error():
    import pytest
    with pytest.raises(ValueError):
        calculate_order_total(-10, 1)
