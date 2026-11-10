from collections.abc import Callable, Iterable

from core.compose import pipe
from core.domain import Order, Product
from core.lazy import iter_orders_by_day, lazy_top_customers


class CatalogService:
    """Фасад для операций с каталогом."""

    def __init__(self, products: tuple[Product, ...], filter_function: Callable = None):
        self.products = products
        self.filter_function = filter_function or (
            lambda items, predicate: tuple(
                product for product in items if predicate(product)
            )
        )

    def filter_products(self, predicate: Callable) -> tuple[Product, ...]:
        return self.filter_function(self.products, predicate)


class OrderService:
    """Фасад для операций с заказами."""

    def __init__(self, orders: tuple[Order, ...], day_filter: Callable = None):
        self.orders = orders
        self.day_filter = day_filter or iter_orders_by_day

    def orders_for_day(self, day: str) -> tuple[Order, ...]:
        return tuple(self.day_filter(self.orders, day))

    def paid_orders_for_day(self, day: str) -> tuple[Order, ...]:
        return pipe(
            self.orders_for_day(day),
            lambda items: tuple(order for order in items if order.status == "paid"),
        )


class AnalyticsService:
    """Фасад аналитики. Функции можно передать извне (DI)."""

    def __init__(
        self,
        orders: tuple[Order, ...],
        day_filter: Callable = None,
        top_customers_function: Callable = None,
    ):
        self.orders = orders
        self.day_filter = day_filter or iter_orders_by_day
        self.top_customers_function = top_customers_function or lazy_top_customers

    def daily_report(self, day: str, top_k: int = 5) -> dict:
        # Каждый шаг создаёт отдельный результат, исходные заказы не меняются.
        day_orders = tuple(self.day_filter(self.orders, day))
        paid_orders = tuple(
            order for order in day_orders if order.status == "paid"
        )
        sales = sum(order.total for order in paid_orders)
        top_customers = tuple(self.top_customers_function(paid_orders, top_k))

        return {
            "day": day,
            "all_orders": day_orders,
            "paid_orders": paid_orders,
            "sales": sales,
            "top_customers": top_customers,
        }
