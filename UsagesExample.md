# Примеры использования

Здесь можно просмотреть результаты выполнения программы

## Вся таблица

```console
python main.py products.csv
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| galaxy a54       | samsung |     349 |      4.2 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| iphone se        | apple   |     429 |      4.1 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
| iphone 13 mini   | apple   |     599 |      4.5 |
+------------------+---------+---------+----------+
```

[Скриншот](result_screenshot/all_table.png)

## Фильтрация: *где рейтинг больше 4.4*
```console
python main.py products.csv --where "rating>4.4"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| iphone 13 mini   | apple   |     599 |      4.5 |
+------------------+---------+---------+----------+
```

[Скриншот](result_screenshot/rating_more_4_4.png)

## Фильтрация: *где брэнд это apple*
```console
python main.py products.csv --where "brand=apple"
+----------------+---------+---------+----------+
| name           | brand   |   price |   rating |
|----------------+---------+---------+----------|
| iphone 15 pro  | apple   |     999 |      4.9 |
| iphone 14      | apple   |     799 |      4.7 |
| iphone se      | apple   |     429 |      4.1 |
| iphone 13 mini | apple   |     599 |      4.5 |
+----------------+---------+---------+----------+
```

[Скриншот](result_screenshot/brand_is_apple.png)

## Фильтрация: *где цена ниже 200*
```console
python main.py products.csv --where "price<200"
+---------------+---------+---------+----------+
| name          | brand   |   price |   rating |
|---------------+---------+---------+----------|
| redmi note 12 | xiaomi  |     199 |      4.6 |
| redmi 10c     | xiaomi  |     149 |      4.1 |
+---------------+---------+---------+----------+
```

[Скриншот](result_screenshot/price_less_200.png)

## Агрегация: *минимальная цена*
```console
python main.py products.csv --aggregate "price=min"
+-------+
|   min |
|-------|
|   149 |
+-------+
```

[Скриншот](result_screenshot/price_min.png)

## Агрегация: *средний рейтинг*
```console
python main.py products.csv --aggregate "rating=avg"
+-------+
|   avg |
|-------|
|  4.49 |
+-------+
```

[Скриншот](result_screenshot/rating_avg.png)

## Агрегация: *максимальный рейтинг*
```console
python main.py products.csv --aggregate "rating=max"
+-------+
|   max |
|-------|
|   4.9 |
+-------+
```

[Скриншот](result_screenshot/rating_max.png)

## Комбинированный пример: *максимальная цена бренда apple*
```console
python main.py products.csv --where "brand=apple" --aggregate "rating=max"
+-------+
|   max |
|-------|
|   4.9 |
+-------+
```

[Скриншот](result_screenshot/apple_max_rating.png)

## Комбинированный пример: *средний рейтинг для цен больше 300*

```console
python main.py products.csv --where "price>300" --aggregate "rating=avg"
+---------+
|     avg |
|---------|
| 4.54286 |
+---------+
```

[Скриншот](result_screenshot/price_more_300_avg_rating.png)

 