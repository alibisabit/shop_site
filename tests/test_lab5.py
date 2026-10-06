from core.domain import Order
from core.lazy import iter_orders_by_day, lazy_top_customers


def make_order(order_id, user_id, total, ts):
    return Order(
        id=order_id,
        user_id=user_id,
        items=(),
        total=total,
        ts=ts,
        status="paid",
    )


def test_iter_orders_by_day():
    orders = (
        make_order("1", "u1", 1000, "2026-10-01T10:00:00"),
        make_order("2", "u2", 2000, "2026-10-02T12:00:00"),
        make_order("3", "u3", 3000, "2026-10-01T15:00:00"),
    )

    result = list(iter_orders_by_day(orders, "2026-10-01"))

    assert len(result) == 2
    assert result[0].id == "1"
    assert result[1].id == "3"


def test_iter_orders_by_day_empty():
    orders = (make_order("1", "u1", 1000, "2026-10-01T10:00:00"),)

    result = list(iter_orders_by_day(orders, "2026-10-05"))

    assert result == []


def test_iter_orders_by_day_is_generator():
    orders = (make_order("1", "u1", 1000, "2026-10-01T10:00:00"),)

    result = iter_orders_by_day(orders, "2026-10-01")

    assert hasattr(result, "__next__")


def test_lazy_top_customers():
    orders = (
        make_order("1", "u1", 1000, "2026-10-01T10:00:00"),
        make_order("2", "u2", 5000, "2026-10-01T11:00:00"),
        make_order("3", "u1", 3000, "2026-10-01T12:00:00"),
    )

    result = list(lazy_top_customers(orders, 2))

    assert result == [("u1", 4000), ("u2", 5000)] or result == [
        ("u2", 5000),
        ("u1", 4000),
    ]


def test_lazy_top_customers_limit():
    orders = (
        make_order("1", "u1", 1000, "2026-10-01T10:00:00"),
        make_order("2", "u2", 5000, "2026-10-01T11:00:00"),
        make_order("3", "u3", 3000, "2026-10-01T12:00:00"),
    )

    result = list(lazy_top_customers(orders, 2))

    assert len(result) == 2


def test_lazy_top_customers_is_generator():
    orders = (make_order("1", "u1", 1000, "2026-10-01T10:00:00"),)

    result = lazy_top_customers(orders, 1)

    assert hasattr(result, "__next__")
