from core.domain import Cart, Order
from core.transforms import (
    add_to_cart,
    remove_from_cart,
    checkout,
    total_sales,
)


def test_add_to_cart():
    cart = Cart("c1", "u1", ())

    new_cart = add_to_cart(cart, "p1", 2)

    assert new_cart.items == (("p1", 2),)


def test_add_existing_product():
    cart = Cart("c1", "u1", (("p1", 2),))

    new_cart = add_to_cart(cart, "p1", 3)

    assert new_cart.items == (("p1", 5),)


def test_remove_from_cart():
    cart = Cart(
        "c1",
        "u1",
        (("p1", 2), ("p2", 1)),
    )

    new_cart = remove_from_cart(cart, "p1")

    assert new_cart.items == (("p2", 1),)


def test_cart_is_immutable():
    cart = Cart("c1", "u1", ())

    new_cart = add_to_cart(cart, "p1", 2)

    assert cart.items == ()
    assert new_cart.items == (("p1", 2),)


def test_total_sales():
    orders = (
        Order("o1", "u1", (), 1000, "2026-09-22", "paid"),
        Order("o2", "u2", (), 2000, "2026-09-22", "paid"),
    )

    assert total_sales(orders) == 3000