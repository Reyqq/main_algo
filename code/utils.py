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
    return (array - array.mean()) / array.std()


@lst_to_array
def get_probabilities(array: np.ndarray, method: str = "default", beta: float = 1.0) -> np.ndarray:
    """Преобразует массив значений в массив вероятностей различными методами.

    Args:
        array (np.ndarray): Входной массив значений (например, оценки или fitness).
                            Декоратор @lst_to_array преобразует список в массив.
        method (str, optional): Метод преобразования. Доступные методы:
            'default': Простое нормирование делением на сумму.
            'rank': Ранговое нормирование (чем выше ранг, тем выше вероятность).
            'softmax': Softmax преобразование с параметром beta.
            'uniform': Равномерное распределение (эквивалентно softmax с beta=0).
            По умолчанию "default".
        beta (float, optional): Параметр для метода 'softmax', контролирующий
                                "резкость" распределения. По умолчанию 1.0.

    Returns:
        np.ndarray: Массив вероятностей, сумма элементов которого равна 1.
    """

    def softmax(arr: np.ndarray, beta_param: float) -> np.ndarray:
        """Внутренняя функция для Softmax преобразования."""
        # Стандартизация перед softmax для численной стабильности
        scaled_arr = standard_scaler(arr)
        exp_array = np.exp(beta_param * scaled_arr)
        probabilities = exp_array / np.sum(exp_array)
        return probabilities
    
    match method:
        case "default":
            probabilities = array / array.sum()
        case "rank":
            reversed_ranks = np.argsort(np.argsort(array)) + 1
            probabilities = reversed_ranks / sum(reversed_ranks)
        case "softmax":
            probabilities = softmax(array, beta)
        case "uniform":
            probabilities = softmax(array, 0)
        case _:
            raise KeyError(f"Unknown {method = }, choose available methods {config.PROBABILITIES_METHODS}.")
    return probabilities


def select_method(config_proba: Dict[str, float]) -> str:
    """Выбирает метод случайным образом на основе заданных вероятностей.

    Args:
        config_proba (Dict[str, float]): Словарь, где ключи - названия методов,
                                         а значения - их вероятности выбора.
                                         Сумма вероятностей должна быть равна 1.

    Returns:
        str: Случайно выбранное название метода.
    """
    methods = list(config_proba.keys())
    probs = list(config_proba.values())
    return np.random.choice(methods, size=1, p=probs).tolist()[0]


def get_action_idxes(n_obs: int, proba: float) -> np.ndarray:
    """Генерирует индексы для выполнения действия на основе вероятности.

    Для каждого из `n_obs` наблюдений генерируется случайное число. Если оно
    меньше `proba`, индекс этого наблюдения добавляется в результат.

    Args:
        n_obs (int): Общее количество наблюдений (или потенциальных действий).
        proba (float): Вероятность выполнения действия для каждого наблюдения (от 0 до 1).

    Returns:
        np.ndarray: Массив целых чисел - индексы наблюдений, для которых
                    должно быть выполнено действие.
    """
    idxes_mask = np.random.rand((n_obs)) < proba
    action_idxes = np.nonzero(idxes_mask)[0]
    return action_idxes


# --- Функции работы с файлами ---

def get_file_rowcols(path: str) -> Tuple[int, int]:
    """Получает количество строк и столбцов для файлов Parquet или HDF5.

    Примечание: Работает только для стандартных табличных структур.
    Для HDF5 предполагается структура 'table/columns' и одинаковое
    количество строк во всех столбцах (проверяется по первому столбцу).

    Args:
        path (str): Путь к файлу (.parquet или .hdf5).

    Returns:
        Tuple[int, int]: Кортеж (количество строк, количество столбцов).
    """
    extension = path.split(".")[-1]
    match extension:
        case "parquet":
            pq_file = pq.ParquetFile(path)
            n_rows = pq_file.metadata.num_rows
            n_cols = pq_file.metadata.num_columns
        case "hdf5": # для файлов где в каждой колонке одинаковое количество строк, я беру количество строк только с первой колонки
            obj = "table/columns"
            with h5py.File(path, "r") as f:
                target_object = f[obj]
                n_cols = len(target_object)
                n_rows = f[obj + "/" + list(target_object.keys())[0] + "/data"].shape[0]
    return n_rows, n_cols

def get_chunks(data: Union[np.ndarray, pd.DataFrame], n_jobs: int, axis: int = 0) -> List[Union[np.ndarray, pd.DataFrame]]:
    """Разбивает данные (NumPy массив или Pandas DataFrame) на части (chunks).

    Args:
        data (Union[np.ndarray, pd.DataFrame]): Входные данные для разбиения.
        n_jobs (int): Количество частей (chunks), на которые нужно разбить данные.
                      Должно быть положительным целым числом.
        axis (int, optional): Ось, по которой происходит разбиение.
                              0 - разбиение по строкам (по умолчанию).
                              1 - разбиение по столбцам (доступно только для DataFrame).
                              По умолчанию 0.

    Returns:
        List[Union[np.ndarray, pd.DataFrame]]: Список частей данных. Тип элементов
                                               списка соответствует типу входных данных.
    """
    if axis == 1 and not isinstance(data, pd.DataFrame):
        raise ValueError("Разбиение по столбцам (axis=1) доступно только для Pandas DataFrame.")
    size = data.shape[1] if axis else len(data)
    chunk_size = size//n_jobs
    chunks = []
    for i in range(0, size, chunk_size):
        chunks.append(data.iloc[:, i : i + chunk_size] if axis else data[i: i + chunk_size])
    return chunks















