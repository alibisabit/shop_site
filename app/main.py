import time

import streamlit as st

from core.memo import top_products
from core.recursion import collect_products_recursive
from core.transforms import (
    by_price_range,
    by_tag,
    load_seed,
    total_sales,
)

st.set_page_config(
    page_title="Аналитика интернет-магазина",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 Аналитика интернет-магазина")

menu = st.sidebar.selectbox(
    "Меню",
    [
        "Overview",
        "Data",
        "Functional Core",
        "Reports",
    ],
)

try:
    (
        categories,
        products,
        users,
        carts,
        orders,
        payments,
        events,
        discounts,
    ) = load_seed("data/seed.json")
except FileNotFoundError:
    st.error("Файл data/seed.json не найден.")
    st.stop()


if menu == "Overview":
    st.header("Обзор")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Пользователи", len(users))
    col2.metric("Товары", len(products))
    col3.metric("Заказы", len(orders))
    col4.metric(
        "Продажи",
        f"{total_sales(orders) / 100:.2f} ₽",
    )


elif menu == "Data":
    st.header("Данные")

    st.subheader("Категории")

    st.dataframe(
        [
            {
                "ID": category.id,
                "Название": category.name,
                "Родитель": category.parent_id,
            }
            for category in categories
        ],
        use_container_width=True,
    )

    st.subheader("Товары")

    st.dataframe(
        [
            {
                "ID": product.id,
                "Название": product.title,
                "Цена": product.price / 100,
                "Категория": product.category_id,
                "Теги": ", ".join(product.tags),
            }
            for product in products
        ],
        use_container_width=True,
    )


elif menu == "Functional Core":
    st.header("Functional Core")

    st.write(
        "Фильтрация каталога с использованием "
        "замыканий и рекурсивного обхода категорий."
    )

    # Фильтр по категории
    category_names = {category.id: category.name for category in categories}

    category_options = {
        "Все категории": None,
        **{
            category.name: category.id
            for category in categories
            if category.parent_id is None
        },
    }

    selected_category = st.selectbox(
        "Категория",
        list(category_options.keys()),
    )

    category_id = category_options[selected_category]

    # Фильтр по цене
    min_price = min(product.price for product in products)
    max_price = max(product.price for product in products)

    price_range = st.slider(
        "Диапазон цены",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=100,
    )

    # Фильтр по тегу
    all_tags = sorted({tag for product in products for tag in product.tags})

    selected_tag = st.selectbox(
        "Тег",
        ["Все теги"] + all_tags,
    )

    # Применяем фильтры
    filtered_products = products

    if category_id is not None:
        filtered_products = collect_products_recursive(
            categories,
            filtered_products,
            category_id,
        )

    price_filter = by_price_range(
        price_range[0],
        price_range[1],
    )

    filtered_products = tuple(
        product for product in filtered_products if price_filter(product)
    )

    if selected_tag != "Все теги":
        tag_filter = by_tag(selected_tag)

        filtered_products = tuple(
            product for product in filtered_products if tag_filter(product)
        )

    st.subheader("Результат")

    st.write(f"Найдено товаров: {len(filtered_products)}")

    st.dataframe(
        [
            {
                "ID": product.id,
                "Название": product.title,
                "Цена": f"{product.price / 100:.2f} ₽",
                "Категория": category_names.get(
                    product.category_id,
                    product.category_id,
                ),
                "Теги": ", ".join(product.tags),
            }
            for product in filtered_products
        ],
        use_container_width=True,
    )

elif menu == "Reports":
    st.header("Reports")

    st.subheader("Top Products (cached)")

    k = st.slider(
        "Количество товаров",
        min_value=1,
        max_value=10,
        value=5,
    )

    top_products.cache_clear()

    start_time = time.perf_counter()

    first_result = top_products(
        orders,
        products,
        k,
    )

    first_time = (time.perf_counter() - start_time) * 1000

    start_time = time.perf_counter()

    second_result = top_products(
        orders,
        products,
        k,
    )

    second_time = (time.perf_counter() - start_time) * 1000

    col1, col2 = st.columns(2)

    col1.metric(
        "Первый вызов",
        f"{first_time:.4f} ms",
    )

    col2.metric(
        "Второй вызов (кэш)",
        f"{second_time:.4f} ms",
    )

    st.write(f"Попаданий в кэш: {top_products.cache_info().hits}")

    st.subheader("Бестселлеры")

    st.dataframe(
        [
            {
                "ID": product.id,
                "Название": product.title,
                "Цена": f"{product.price / 100:.2f} ₽",
                "Категория": product.category_id,
            }
            for product in second_result
        ],
        use_container_width=True,
    )
