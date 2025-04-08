# -*- coding: utf-8 -*-
import numpy as np
from typing import Union, List

def sample_function(x: Union[int, float], y: str = "default") -> float:
    """
    Это пример функции для демонстрации документации.

    Она принимает число и строку и возвращает число.

    Args:
        x: Входное число (int или float).
        y: Входная строка (str), по умолчанию "default".

    Returns:
        Квадрат входного числа x.

    Raises:
        TypeError: Если x не является числом.
    """
    if not isinstance(x, (int, float)):
        raise TypeError("Параметр 'x' должен быть числом.")
    print(f"Вызвана функция с x={x}, y='{y}'")
    return float(x**2)

class SampleClass:
    """
    Пример класса для документации.

    Attributes:
        value (float): Хранимое значение.
    """
    def __init__(self, initial_value: float = 0.0):
        """Инициализирует класс."""
        self.value = initial_value
        print(f"Создан экземпляр SampleClass со значением {self.value}")

    def add(self, number: float) -> None:
        """
        Добавляет число к хранимому значению.

        Args:
            number: Число для добавления.
        """
        self.value += number
        print(f"Новое значение: {self.value}")