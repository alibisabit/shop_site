from core.domain import Category, Product


def flatten_categories(
    cats: tuple[Category, ...],
    root: str,
) -> tuple[Category, ...]:
    current = tuple(category for category in cats if category.id == root)

    children = tuple(category for category in cats if category.parent_id == root)

    result = current

    for child in children:
        result = result + flatten_categories(cats, child.id)

    return result


def collect_products_recursive(
    cats: tuple[Category, ...],
    prods: tuple[Product, ...],
    root_id: str,
) -> tuple[Product, ...]:
    categories = flatten_categories(cats, root_id)

    category_ids = tuple(category.id for category in categories)

    return tuple(product for product in prods if product.category_id in category_ids)
