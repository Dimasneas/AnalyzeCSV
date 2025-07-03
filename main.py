import argparse
from table_query import Table
import re


def parse_expression(expr: str, pattern: str) -> list[str]:
    """
    Разбирает выражение по регулярному выражению, и возвращает список компонентов.

    :param expr: строка выражения (например, 'age>30')
    :param pattern: регулярное выражение для разбора
    :return: список из разбитых компонентов
    :raises ValueError: если строка не соответствует шаблону
    """
    match = re.fullmatch(pattern, expr)
    if not match:
        raise ValueError(f"Неверный формат: {expr}")
    return [s.strip() for s in match.groups()]


def main():
    parser = argparse.ArgumentParser(
        prog="main",
        description="Работа с CSV-таблицей: фильтрация и агрегаты",
        epilog="""
        Примеры использования:
            python main.py data.csv
            python main.py data.csv --where 'age>30'
            python main.py data.csv -a 'salary=avg'
            python main.py -f data.csv -w 'name=Mike' -a 'age=max'
        """
    )

    parser.add_argument("file", nargs="?",
                        help="Путь к CSV-файлу")
    parser.add_argument("--file", "-f", dest="file_flag",
                        help="Путь к CSV-файлу (альтернатива позиционному)")
    parser.add_argument("--where", "-w", metavar="COLUMN=VALUE",
                        help="Фильтрация: column=val, column>val и т.д.")
    parser.add_argument("--aggregate", "-a", metavar="COLUMN=FUNC",
                        help="Агрегация: column=avg, column=min, column=max")


    args = parser.parse_args()

    filename = args.file or args.file_flag
    if not filename:
        parser.error("Необходимо указать CSV-файл через --file или как позиционный аргумент.")

    table = Table.from_csv(filename)

    if args.where:
        try:
            column, operator, value = parse_expression(args.where, r"(.+?)([!<>=]{1,2})(.+)")
            table = table.filter(column, operator, value)
        except (ValueError, KeyError, TypeError) as e:
            parser.error(f"Ошибка фильтрации. {e}")
    if args.aggregate:
        try:
            column, func = parse_expression(args.aggregate, r"(.+?)=(avg|min|max)")
            table = table.aggregate(column, func)
        except (ValueError, KeyError, TypeError) as e:
            parser.error(f"Ошибка агрегирования. {e}")

    print(table)


if __name__ == "__main__":
    main()
