from core.domain import Category, Product, User
from core.recursion import (
    collect_products_recursive,
    flatten_categories,
)
from core.transforms import (
    by_category,
    by_price_range,
    by_tag,
    by_user_tier,
)


def test_by_category():
    product = Product(
        id="p1",
        title="Phone",
        price=50000,
        category_id="cat3",
        tags=("phone",),
    )

    filter_func = by_category("cat3")

    assert filter_func(product) is True
    assert by_category("cat2")(product) is False


def test_by_price_range():
    product = Product(
        id="p1",
        title="Phone",
        price=50000,
        category_id="cat3",
        tags=("phone",),
    )

    filter_func = by_price_range(40000, 60000)

    assert filter_func(product) is True
    assert by_price_range(60000, 70000)(product) is False


def test_by_tag():
    product = Product(
        id="p1",
        title="Phone",
        price=50000,
        category_id="cat3",
        tags=("phone", "smart"),
    )

    assert by_tag("phone")(product) is True
    assert by_tag("laptop")(product) is False


def test_by_user_tier():
    user = User(
        id="u1",
        name="Alex",
        tier="VIP",
    )

    assert by_user_tier("VIP")(user) is True
    assert by_user_tier("regular")(user) is False


def test_flatten_categories():
    categories = (
        Category("cat1", "Electronics", None),
        Category("cat2", "Laptops", "cat1"),
        Category("cat3", "Phones", "cat1"),
        Category("cat4", "Headphones", "cat1"),
    )

    result = flatten_categories(categories, "cat1")

    assert len(result) == 4
    assert result[0].id == "cat1"
    assert result[1].id == "cat2"
    assert result[2].id == "cat3"
    assert result[3].id == "cat4"


def test_collect_products_recursive():
    categories = (
        Category("cat1", "Electronics", None),
        Category("cat2", "Laptops", "cat1"),
        Category("cat3", "Phones", "cat1"),
    )

    products = (
        Product("p1", "Laptop", 100000, "cat2", ("computer",)),
        Product("p2", "Phone", 50000, "cat3", ("phone",)),
        Product("p3", "Book", 20000, "cat8", ("book",)),
    )

    result = collect_products_recursive(
        categories,
        products,
        "cat1",
    )

    assert len(result) == 2
    assert result[0].id == "p1"
    assert result[1].id == "p2"
