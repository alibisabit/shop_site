from core.domain import Order, Product
from core.ftypes import Either, Maybe, safe_product, validate_order


def test_maybe_map():
    result = Maybe(5).map(lambda x: x * 2)

    assert result.value == 10


def test_maybe_map_empty():
    result = Maybe(None).map(lambda x: x * 2)

    assert result.value is None


def test_maybe_get_or_else():
    result = Maybe(None).get_or_else(100)

    assert result == 100


def test_safe_product_found():
    products = (
        Product("p1", "Телефон", 10000, "c1", ("tech",)),
        Product("p2", "Ноутбук", 20000, "c1", ("tech",)),
    )

    result = safe_product(products, "p1")

    assert result.value is not None
    assert result.value.id == "p1"


def test_safe_product_not_found():
    products = (Product("p1", "Телефон", 10000, "c1", ("tech",)),)

    result = safe_product(products, "p999")

    assert result.value is None


def test_validate_order_success():
    order = Order(
        "o1",
        "u1",
        (("p1", 2),),
        20000,
        "2026-09-26",
        "paid",
    )

    result = validate_order(order, {"p1": 5}, ())

    assert result.value == order
    assert result.error is None


def test_validate_order_not_enough_stock():
    order = Order(
        "o1",
        "u1",
        (("p1", 5),),
        50000,
        "2026-09-26",
        "paid",
    )

    result = validate_order(order, {"p1": 2}, ())

    assert result.value is None
    assert result.error is not None


def test_either_get_or_else():
    result = Either.left("Ошибка").get_or_else("Значение по умолчанию")

    assert result == "Значение по умолчанию"
