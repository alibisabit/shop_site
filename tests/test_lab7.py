from core.compose import compose, pipe
from core.domain import Order, Product
from core.service import AnalyticsService, CatalogService, OrderService


def make_order(order_id, user_id, total, ts, status="paid"):
    return Order(order_id, user_id, (), total, ts, status)


def test_pipe_runs_functions_left_to_right():
    result = pipe(3, lambda x: x + 2, lambda x: x * 4)
    assert result == 20


def test_compose_runs_functions_right_to_left():
    function = compose(lambda x: x * 4, lambda x: x + 2)
    assert function(3) == 20


def test_catalog_service_filters_products():
    products = (
        Product("p1", "Phone", 1000, "c1", ()),
        Product("p2", "Book", 500, "c2", ()),
    )
    service = CatalogService(products)
    result = service.filter_products(lambda product: product.price >= 1000)
    assert tuple(product.id for product in result) == ("p1",)


def test_order_service_returns_paid_orders_for_day():
    orders = (
        make_order("1", "u1", 1000, "2026-10-01T10:00:00"),
        make_order("2", "u2", 2000, "2026-10-01T11:00:00", "refunded"),
        make_order("3", "u3", 3000, "2026-10-02T10:00:00"),
    )
    service = OrderService(orders)
    result = service.paid_orders_for_day("2026-10-01")
    assert tuple(order.id for order in result) == ("1",)


def test_analytics_service_daily_report():
    orders = (
        make_order("1", "u1", 1000, "2026-10-01T10:00:00"),
        make_order("2", "u1", 2000, "2026-10-01T11:00:00"),
        make_order("3", "u2", 5000, "2026-10-01T12:00:00", "refunded"),
    )
    report = AnalyticsService(orders).daily_report("2026-10-01", 2)
    assert len(report["all_orders"]) == 3
    assert len(report["paid_orders"]) == 2
    assert report["sales"] == 3000
    assert report["top_customers"] == (("u1", 3000),)


def test_services_accept_dependencies():
    products = (Product("p1", "Phone", 1000, "c1", ()),)
    custom_filter = lambda items, predicate: ("custom",)
    service = CatalogService(products, filter_function=custom_filter)
    assert service.filter_products(lambda product: True) == ("custom",)
