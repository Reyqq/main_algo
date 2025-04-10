"""Модуль вспомогательных утилит.

Содержит функции для сериализации, преобразования типов данных,
масштабирования, вычисления вероятностей, работы с файлами и данными.
"""

import h5py
import pickle
import numpy as np
import pandas as pd
import pyarrow.parquet as pq


from functools import wraps
from typing import Any, List, Dict, Tuple, Callable, Union, Sequence


# --- Сериализация ---

def save_pickle(obj: Any, path: str) -> None:
    """Сохраняет объект Python в файл с использованием pickle.

    Args:
        obj (Any): Объект Python для сохранения.
        path (str): Путь к файлу, в который будет сохранен объект.
                    Расширение файла обычно .pkl или .pickle.
    """
    pickle.dump(obj, open(f"{path}", "wb"))


def load_pickle(path: str) -> Any:
    """Загружает объект Python из файла pickle.

    Args:
        path (str): Путь к файлу pickle для загрузки.

    Returns:
        Any: Загруженный объект Python.
    """
    return pickle.load(open(f"{path}", "rb"))

# --- Декораторы для преобразования типов ---

def lst_to_array(function: Callable) -> Callable:
    """Декоратор для преобразования списков в NumPy массивы в аргументах функции."""
    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Обертка, преобразующая списки в массивы."""
        new_args = [np.asarray(a) if isinstance(a, list) else a for a in args]
        new_kwargs = {k: np.asarray(v) if isinstance(v, list) else v for k, v in kwargs.items()}
        return function(*new_args, **new_kwargs)
    return wrapper


def array_to_lst(function):
    """Декоратор для преобразования NumPy массивов в списки в аргументах функции."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        """Обертка, преобразующая массивы в списки."""
        args = [a.tolist() if isinstance(a, np.ndarray) else a for a in args]
        kwargs = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in kwargs.items()}
        return function(*args, **kwargs)
    return wrapper

# --- Функции обработки данных ---


@lst_to_array
def standard_scaler(array: np.ndarray) -> np.ndarray:
    """Стандартизирует массив (вычитает среднее и делит на стандартное отклонение).

    Применяет стандартизацию (Z-score normalization).

    Args:
        array (np.ndarray): Входной NumPy массив для стандартизации.
                            Декоратор @lst_to_array преобразует список в массив, если нужно.

    Returns:
        np.ndarray: Стандартизированный массив. Имеет среднее ~0 и стд. отклонение ~1.
    """
    return (array - array.mean())/array.std()





