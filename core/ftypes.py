from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from core.domain import Discount, Order, Product

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True)
class Maybe(Generic[T]):
    value: T | None

    def map(self, func: Callable[[T], U]) -> "Maybe[U]":
        if self.value is None:
            return Maybe(None)
        return Maybe(func(self.value))

    def bind(self, func: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        if self.value is None:
            return Maybe(None)
        return func(self.value)

    def get_or_else(self, default: U) -> T | U:
        if self.value is None:
            return default
        return self.value


@dataclass(frozen=True)
class Either(Generic[T]):
    value: T | None
    error: str | None = None

    @classmethod
    def right(cls, value: T) -> "Either[T]":
        return cls(value=value)

    @classmethod
    def left(cls, error: str) -> "Either[T]":
        return cls(value=None, error=error)

    def map(self, func: Callable[[T], U]) -> "Either[U]":
        if self.error is not None:
            return Either.left(self.error)
        return Either.right(func(self.value))

    def bind(self, func: Callable[[T], "Either[U]"]) -> "Either[U]":
        if self.error is not None:
            return Either.left(self.error)
        return func(self.value)

    def get_or_else(self, default: U) -> T | U:
        if self.error is not None:
            return default
        return self.value


def safe_product(products: tuple[Product, ...], pid: str) -> Maybe[Product]:
    for product in products:
        if product.id == pid:
            return Maybe(product)

    return Maybe(None)


def validate_order(
    order: Order,
    stock: dict[str, int],
    discounts: tuple[Discount, ...],
) -> Either[Order]:
    for product_id, quantity in order.items:
        available = stock.get(product_id, 0)

        if quantity <= 0:
            return Either.left(f"Некорректное количество товара: {product_id}")

        if available < quantity:
            return Either.left(
                f"Недостаточно товара {product_id}: "
                f"нужно {quantity}, есть {available}"
            )

    if order.total < 0:
        return Either.left("Сумма заказа не может быть отрицательной")

    return Either.right(order)
