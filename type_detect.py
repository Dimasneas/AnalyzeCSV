"""
:mod:`type_detect`

Модуль предоставляет функцию определения предполагаемого типа значения на основе попытки приведения.

Для добавления новых типов:
    1. Определите функцию, принимающую строку и возвращающую нужный тип, выбрасывая исключение при ошибке.
    2. Добавьте эту функцию в список `_TYPE_TRIES` в порядке приоритета.

Пример добавления:
    def _to_bool(value: str) -> bool:
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        raise ValueError

    _TYPE_TRIES = [int, float, _to_bool]


Функция:
    :func:`detect_type` -- возвращает int, float или str в зависимости от успешного преобразования.
"""

from typing import Type

_TYPE_TRIES = [int, float]


def detect_type(value: str) -> Type:
    """
    Определяет предполагаемый тип значения на основе попытки преобразования.

    :func:`detect_type` возвращает первый подходящий тип из списка поддерживаемых типов.

    :param value: Строковое значение.
    :return: Определённый тип (int, float или str).
    """
    for typ in _TYPE_TRIES:
        try:
            typ(value)
            return typ
        except (ValueError, TypeError):
            continue
    return str
