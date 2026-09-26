from functools import reduce
from core.domain import Cart, Order
import json
from core.domain import Category, Product, User, Order



def add_to_cart(cart: Cart, product_id: str, qty: int) -> Cart:
    new_items = list(cart.items)

    for i, (pid, old_qty) in enumerate(new_items):
        if pid == product_id:
            new_items[i] = (pid, old_qty + qty)
            return Cart(cart.id, cart.user_id, tuple(new_items))

    new_items.append((product_id, qty))

    return Cart(cart.id, cart.user_id, tuple(new_items))


def remove_from_cart(cart: Cart, product_id: str) -> Cart:
    new_items = tuple(
        (pid, qty)
        for pid, qty in cart.items
        if pid != product_id
    )

    return Cart(cart.id, cart.user_id, new_items)


def checkout(cart: Cart, ts: str) -> Order:
    total = sum(qty for _, qty in cart.items)

    return Order(
        id=f"order-{cart.id}",
        user_id=cart.user_id,
        items=cart.items,
        total=total,
        ts=ts,
        status="paid",
    )


def total_sales(orders: tuple[Order, ...]) -> int:
    return reduce(
        lambda total, order: total + order.total,
        orders,
        0,
    )


    


def load_seed(path: str):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = tuple(
        Category(
            item["id"],
            item["name"],
            item["parent_id"],
        )
        for item in data["categories"]
    )

    products = tuple(
        Product(
            item["id"],
            item["title"],
            item["price"],
            item["category_id"],
            tuple(item["tags"]),
        )
        for item in data["products"]
    )

    users = tuple(
        User(
            item["id"],
            item["name"],
            item["tier"],
        )
        for item in data["users"]
    )

    return categories, products, users