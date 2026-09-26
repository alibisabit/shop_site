from core.domain import Order, Product
from core.memo import top_products


def make_products():
    return (
        Product("p1", "Phone", 50000, "cat3", ("phone",)),
        Product("p2", "Laptop", 100000, "cat2", ("laptop",)),
        Product("p3", "Book", 20000, "cat8", ("book",)),
    )


def make_orders():
    return (
        Order(
            "o1",
            "u1",
            (("p1", 3), ("p2", 1)),
            250000,
            "2026-09-01",
            "paid",
        ),
        Order(
            "o2",
            "u2",
            (("p1", 2), ("p3", 5)),
            200000,
            "2026-09-02",
            "paid",
        ),
        Order(
            "o3",
            "u3",
            (("p2", 10),),
            1000000,
            "2026-09-03",
            "cancelled",
        ),
    )


def test_top_products_returns_products():
    result = top_products(make_orders(), make_products())

    assert isinstance(result, tuple)
    assert all(isinstance(product, Product) for product in result)


def test_top_products_sorting():
    result = top_products(make_orders(), make_products())

    assert result[0].id == "p1"
    assert result[1].id == "p3"


def test_top_products_respects_k():
    result = top_products(
        make_orders(),
        make_products(),
        k=1,
    )

    assert len(result) == 1
    assert result[0].id == "p1"


def test_cancelled_orders_are_ignored():
    top_products.cache_clear()

    orders = (
        Order(
            "o1",
            "u1",
            (("p1", 3),),
            150000,
            "2026-09-01",
            "paid",
        ),
        Order(
            "o2",
            "u2",
            (("p2", 10),),
            1000000,
            "2026-09-02",
            "cancelled",
        ),
    )

    result = top_products(
        orders,
        make_products(),
    )

    product_ids = tuple(product.id for product in result)

    assert "p1" in product_ids
    assert "p2" not in product_ids


def test_unknown_product_is_ignored():
    orders = (
        Order(
            "o1",
            "u1",
            (("unknown", 10), ("p1", 2)),
            100000,
            "2026-09-01",
            "paid",
        ),
    )

    result = top_products(
        orders,
        make_products(),
    )

    assert len(result) == 1
    assert result[0].id == "p1"


def test_cache_is_used():
    top_products.cache_clear()

    orders = make_orders()
    products = make_products()

    top_products(orders, products)

    first_info = top_products.cache_info()

    top_products(orders, products)

    second_info = top_products.cache_info()

    assert second_info.hits == first_info.hits + 1
