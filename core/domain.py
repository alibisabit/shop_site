from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    id: str
    name: str
    parent_id: str | None


@dataclass(frozen=True)
class Product:
    id: str
    title: str
    price: int
    category_id: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class User:
    id: str
    name: str
    tier: str


@dataclass(frozen=True)
class Cart:
    id: str
    user_id: str
    items: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class Order:
    id: str
    user_id: str
    items: tuple[tuple[str, int], ...]
    total: int
    ts: str
    status: str