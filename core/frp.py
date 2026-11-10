from collections.abc import Callable
from typing import NamedTuple


class EventMessage(NamedTuple):
    """Событие, которое передаётся через шину."""

    name: str
    ts: str
    payload: dict


Handler = Callable[[EventMessage, dict], dict]


class EventBus:
    """Хранит подписчиков и передаёт им опубликованные события."""

    def __init__(self, state: dict | None = None):
        self.state = state or {}
        self.subscribers: dict[str, list[Handler]] = {}

    def subscribe(self, name: str, handler: Handler) -> None:
        self.subscribers.setdefault(name, []).append(handler)

    def publish(self, name: str, payload: dict, ts: str = "") -> dict:
        event = EventMessage(name=name, ts=ts, payload=payload)

        for handler in self.subscribers.get(name, []):
            self.state = handler(event, self.state)

        return self.state


def add_to_cart_handler(event: EventMessage, state: dict) -> dict:
    """Добавляет товар в копию списка корзин."""
    carts = dict(state.get("carts", {}))
    user_id = event.payload["user_id"]
    items = list(carts.get(user_id, []))
    items.append((event.payload["product_id"], event.payload.get("qty", 1)))
    carts[user_id] = items

    return {**state, "carts": carts}


def remove_handler(event: EventMessage, state: dict) -> dict:
    """Удаляет товар из корзины пользователя."""
    carts = dict(state.get("carts", {}))
    user_id = event.payload["user_id"]
    product_id = event.payload["product_id"]
    items = [
        item for item in carts.get(user_id, [])
        if item[0] != product_id
    ]
    carts[user_id] = items

    return {**state, "carts": carts}


def checkout_handler(event: EventMessage, state: dict) -> dict:
    """Добавляет сумму оформленного заказа к продажам."""
    sales = state.get("sales", 0) + event.payload.get("total", 0)
    return {**state, "sales": sales}


def refund_handler(event: EventMessage, state: dict) -> dict:
    """Учитывает сумму возврата отдельно от продаж."""
    refunds = state.get("refunds", 0) + event.payload.get("total", 0)
    return {**state, "refunds": refunds}


def create_store_bus(state: dict | None = None) -> EventBus:
    """Создаёт шину с готовыми подписчиками магазина."""
    bus = EventBus(state)
    bus.subscribe("ADD_TO_CART", add_to_cart_handler)
    bus.subscribe("REMOVE", remove_handler)
    bus.subscribe("CHECKOUT", checkout_handler)
    bus.subscribe("REFUND", refund_handler)
    return bus
