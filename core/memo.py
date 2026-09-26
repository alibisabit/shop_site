from functools import lru_cache

from core.domain import Order, Product


@lru_cache
def top_products(
    orders: tuple[Order, ...],
    products: tuple[Product, ...],
    k: int = 10,
) -> tuple[Product, ...]:
    sales = {}

    for order in orders:
        if order.status != "paid":
            continue

        for product_id, quantity in order.items:
            sales[product_id] = sales.get(product_id, 0) + quantity

    product_by_id = {product.id: product for product in products}

    sorted_ids = sorted(
        sales,
        key=lambda product_id: sales[product_id],
        reverse=True,
    )

    return tuple(
        product_by_id[product_id]
        for product_id in sorted_ids[:k]
        if product_id in product_by_id
    )
