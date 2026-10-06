from collections import defaultdict
from collections.abc import Iterable, Iterator

from core.domain import Order


def iter_orders_by_day(orders: Iterable[Order], day: str) -> Iterator[Order]:
    for order in orders:
        if order.ts.startswith(day):
            yield order


def lazy_top_customers(orders: Iterable[Order], k: int) -> Iterator[tuple[str, int]]:
    totals = defaultdict(int)

    for order in orders:
        totals[order.user_id] += order.total

    result = sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    yield from result[:k]
