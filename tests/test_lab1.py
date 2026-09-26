from core.domain import Cart, Order
from core.transforms import (
    add_to_cart,
    checkout,
    remove_from_cart,
    total_sales,
)


def test_add_to_cart():
    cart = Cart(
        id="cart1",
        user_id="u1",
        items=(("p1", 2),),
    )

    new_cart = add_to_cart(cart, "p2", 1)

    assert new_cart.items == (
        ("p1", 2),
        ("p2", 1),
    )


def test_add_to_cart_does_not_change_old_cart():
    cart = Cart(
        id="cart1",
        user_id="u1",
        items=(("p1", 2),),
    )

    add_to_cart(cart, "p2", 1)

    assert cart.items == (("p1", 2),)


def test_remove_from_cart():
    cart = Cart(
        id="cart1",
        user_id="u1",
        items=(
            ("p1", 2),
            ("p2", 1),
        ),
    )

    new_cart = remove_from_cart(cart, "p1")

    assert new_cart.items == (("p2", 1),)


def test_checkout():
    cart = Cart(
        id="cart1",
        user_id="u1",
        items=(("p1", 2),),
    )

    order = checkout(
        cart,
        "2026-09-26T16:00:00",
    )

    assert isinstance(order, Order)
    assert order.user_id == "u1"
    assert order.items == (("p1", 2),)
    assert order.status == "paid"


def test_total_sales():
    orders = (
        Order(
            id="order1",
            user_id="u1",
            items=(("p1", 1),),
            total=1000,
            ts="2026-09-20",
            status="paid",
        ),
        Order(
            id="order2",
            user_id="u2",
            items=(("p2", 1),),
            total=2000,
            ts="2026-09-21",
            status="paid",
        ),
    )

    assert total_sales(orders) == 3000
