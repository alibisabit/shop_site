import json
from functools import reduce

from core.domain import (
    Cart,
    Category,
    Discount,
    Event,
    Order,
    Payment,
    Product,
    User,
)


def load_seed(path: str):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = tuple(
        Category(
            id=item["id"],
            name=item["name"],
            parent_id=item["parent_id"],
        )
        for item in data["categories"]
    )

    products = tuple(
        Product(
            id=item["id"],
            title=item["title"],
            price=item["price"],
            category_id=item["category_id"],
            tags=tuple(item["tags"]),
        )
        for item in data["products"]
    )

    users = tuple(
        User(
            id=item["id"],
            name=item["name"],
            tier=item["tier"],
        )
        for item in data["users"]
    )

    carts = tuple(
        Cart(
            id=item["id"],
            user_id=item["user_id"],
            items=tuple(
                (product_id, quantity) for product_id, quantity in item["items"]
            ),
        )
        for item in data["carts"]
    )

    orders = tuple(
        Order(
            id=item["id"],
            user_id=item["user_id"],
            items=tuple(
                (product_id, quantity) for product_id, quantity in item["items"]
            ),
            total=item["total"],
            ts=item["ts"],
            status=item["status"],
        )
        for item in data["orders"]
    )

    payments = tuple(
        Payment(
            id=item["id"],
            order_id=item["order_id"],
            amount=item["amount"],
            ts=item["ts"],
            method=item["method"],
        )
        for item in data["payments"]
    )

    events = tuple(
        Event(
            id=item["id"],
            ts=item["ts"],
            name=item["name"],
            payload=item["payload"],
        )
        for item in data["events"]
    )

    discounts = tuple(
        Discount(
            id=item["id"],
            code=item["code"],
            percent=item["percent"],
            conditions=item["conditions"],
        )
        for item in data["discounts"]
    )

    return (
        categories,
        products,
        users,
        carts,
        orders,
        payments,
        events,
        discounts,
    )


def add_to_cart(cart: Cart, product_id: str, qty: int) -> Cart:
    new_items = cart.items + ((product_id, qty),)

    return Cart(
        id=cart.id,
        user_id=cart.user_id,
        items=new_items,
    )


def remove_from_cart(cart: Cart, product_id: str) -> Cart:
    new_items = tuple(item for item in cart.items if item[0] != product_id)

    return Cart(
        id=cart.id,
        user_id=cart.user_id,
        items=new_items,
    )


def checkout(cart: Cart, ts: str) -> Order:
    return Order(
        id=f"order_{cart.id}",
        user_id=cart.user_id,
        items=cart.items,
        total=0,
        ts=ts,
        status="paid",
    )


def total_sales(orders: tuple[Order, ...]) -> int:
    return reduce(
        lambda total, order: total + order.total,
        orders,
        0,
    )


def by_category(cat_id: str):
    return lambda product: product.category_id == cat_id


def by_price_range(min_price: int, max_price: int):
    return lambda product: min_price <= product.price <= max_price


def by_tag(tag: str):
    return lambda product: tag in product.tags


def by_user_tier(tier: str):
    return lambda user: user.tier == tier
