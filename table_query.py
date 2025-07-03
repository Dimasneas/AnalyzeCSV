"""
:mod:`table_query`

Модуль предоставляет класс Table для работы с табличными данными из CSV-файлов.

Функциональность:
    * Загрузка данных из CSV
    * Автоматическое определение типов данных в столбцах
    * Фильтрация строк по условию
    * Вычисление среднего, минимального и максимального значений
    * Форматированный вывод таблицы

Класс:
    :class:`Table` -- основной интерфейс для обработки и анализа CSV-данных
"""

from csv import DictReader
import operator as op
from typing import Any, List, Dict
from tabulate import tabulate
from type_detect import detect_type

TableData = List[Dict[str, Any]]


class Table:
    """
    Представляет табличные данные с возможностью фильтрации и вычисления статистики.

    :cvar OPS: Словарь операторов сравнения и соответствующих функций.
    :ivar data: Список строк таблицы (словарей).
    :ivar column_types: Предполагаемые типы данных по столбцам.
    """

    OPS = {
        '>': op.gt,
        '<': op.lt,
        '=': op.eq,
    }

    def __init__(self, data: TableData):
        """
        Инициализация таблицы по списку словарей.

        :param data: Список строк таблицы, где каждая строка — словарь.
        """
        self.data = data
        self.column_types = self._get_columns_types()

    @classmethod
    def from_csv(cls, filename: str, delimiter: str = ',') -> 'Table':
        """
        Создаёт объект Table из CSV-файла.

        :param filename: Имя CSV-файла.
        :param delimiter: Разделитель столбцов (по умолчанию ',').
        :return: Новый экземпляр таблицы.
        """
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = DictReader(csvfile, delimiter=delimiter)
            return cls(list(reader))

    def _get_columns_types(self) -> Dict[str, type]:
        """
        Определяет типы данных для каждого столбца по первой строке.

        :return: Сопоставление имён столбцов и предполагаемых типов.
        """
        if not self.data:
            return {}
        example_row = self.data[0]
        types = {}
        for column, value in example_row.items():
            types[column] = detect_type(value)
        return types

    def filter(self, column: str, operator_symbol: str, value: str) -> 'Table':
        """
        Фильтрует строки таблицы по условию.

        :param column: Имя столбца.
        :param operator_symbol: Оператор сравнения ('>', '<', '=').
        :param value: Значение для сравнения.
        :return: Новая таблица с отфильтрованными строками.
        :raises ValueError: Если указан неподдерживаемый оператор сравнения.
        """
        condition = self.OPS.get(operator_symbol)
        if condition is None:
            raise ValueError(f"Неподдерживаемый оператор: {operator_symbol}")
        col_type = self.column_types[column]
        filtered = [row for row in self.data if condition(col_type(row[column]), col_type(value))]
        return Table(filtered)

    def aggregate(self, column: str, func: str) -> 'Table':
        """
        Универсальный метод агрегирования для числовых столбцов.

        :param column: Название столбца.
        :param func: Название агрегатной функции: 'avg', 'min', 'max'.
        :return: Словарь с ключом func и соответствующим значением.
        :raises ValueError: Если функция не поддерживается.
        :raises TypeError: Если столбец не числовой.
        """
        operations = {
            'avg': self.avg,
            'min': self.min,
            'max': self.max
        }

        if func not in operations:
            raise ValueError(f"Неподдерживаемая функция агрегирования: {func}")

        return Table([{func: operations[func](column)}])

    def avg(self, column: str) -> float:
        """
        Вычисляет среднее значение по числовому столбцу.

        :param column: Название столбца.
        :return: Среднее значение.
        :raises TypeError: Если столбец не числовой.
        """
        if self.column_types[column] not in (int, float):
            raise TypeError(f"Столбец '{column}' не числовой и не может быть усреднён.")
        values = [float(row[column]) for row in self.data]
        return sum(values) / len(values)

    def min(self, column: str) -> float:
        """
        ВВозвращает минимальное значение в числовом столбце.

        :param column: Название столбца.
        :return: Минимальное значение.
        :raises TypeError: Если столбец не числовой.
        """
        if self.column_types.get(column) not in (int, float):
            raise TypeError(f"Столбец '{column}' не числовой и не может использоваться для min().")
        values = [float(row[column]) for row in self.data]
        return min(values)

    def max(self, column: str) -> float:
        """
        Возвращает максимальное значение в числовом столбце.

        :param column: Название столбца.
        :return: Максимальное значение.
        :raises TypeError: Если столбец не числовой.
        """
        if self.column_types.get(column) not in (int, float):
            raise TypeError(f"Столбец '{column}' не числовой и не может использоваться для max().")
        values = [float(row[column]) for row in self.data]
        return max(values)

    def __str__(self) -> str:
        return tabulate(self.data, headers='keys', tablefmt='psql')
