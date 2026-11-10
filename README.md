# Аналитика интернет-магазина

## Запуск проекта (Windows)

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m streamlit run app/main.py
```

## Проверка тестов

```bash
python -m pytest -q
```

## Лабораторная №6 — FRP

- `core/frp.py` — EventBus, события и функции-подписчики.
- В меню Streamlit откройте **Async/FRP**.
- Можно сгенерировать ADD_TO_CART, REMOVE, CHECKOUT и REFUND.
- Панели показывают состояние корзин, сумму продаж и сумму возвратов.
- Тесты: `tests/test_lab6.py`.

## Лабораторная №7 — композиция и сервисы

- `core/compose.py` — функции `compose` и `pipe`.
- `core/service.py` — фасады CatalogService, OrderService и AnalyticsService.
- Зависимости можно передавать в конструкторы сервисов.
- В меню Streamlit откройте **Services / Daily Report**.
- Тесты: `tests/test_lab7.py`.

## Лабораторные №1–5

Предыдущие модули и тесты сохранены без переписывания.
