from core.frp import (
    EventBus,
    add_to_cart_handler,
    checkout_handler,
    create_store_bus,
    refund_handler,
)


def test_subscribe_and_publish_event():
    bus = EventBus()
    bus.subscribe("CHECKOUT", checkout_handler)
    result = bus.publish("CHECKOUT", {"total": 1500})
    assert result["sales"] == 1500


def test_add_to_cart_event():
    bus = create_store_bus()
    bus.publish(
        "ADD_TO_CART",
        {"user_id": "u1", "product_id": "p1", "qty": 2},
    )
    assert bus.state["carts"]["u1"] == [("p1", 2)]


def test_remove_event():
    bus = create_store_bus()
    bus.publish("ADD_TO_CART", {"user_id": "u1", "product_id": "p1"})
    bus.publish("ADD_TO_CART", {"user_id": "u1", "product_id": "p2"})
    bus.publish("REMOVE", {"user_id": "u1", "product_id": "p1"})
    assert bus.state["carts"]["u1"] == [("p2", 1)]


def test_checkout_event_updates_sales():
    bus = create_store_bus()
    bus.publish("CHECKOUT", {"total": 2500})
    bus.publish("CHECKOUT", {"total": 500})
    assert bus.state["sales"] == 3000


def test_refund_event_updates_refunds():
    bus = create_store_bus()
    bus.publish("REFUND", {"total": 700})
    assert bus.state["refunds"] == 700


def test_handler_does_not_change_old_state():
    old_state = {"sales": 100}
    new_state = checkout_handler(
        type("Event", (), {"payload": {"total": 50}})(),
        old_state,
    )
    assert old_state == {"sales": 100}
    assert new_state["sales"] == 150
