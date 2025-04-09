"""
Модуль bokehs предоставляет набор функций для создания и настройки финансовых графиков
с использованием библиотеки Bokeh.

Основные функции:
- create_data_sources: Подготовка данных для свечных графиков
- create_candlestick_chart: Создание базового свечного графика
- style_plot: Настройка стиля графика
"""

from typing import Optional, List, Tuple, Dict, Any, Union

import numpy as np
import pandas as pd

def create_data_sources(df: pd.DataFrame) -> Tuple[pd.DataFrame, ColumnDataSource, ColumnDataSource, ColumnDataSource]:
    """


    Создает источники данных для графиков свечей.

    Эта функция обрабатывает входной датафрейм, добавляя новые столбцы для визуализации свечей,
    и создает отдельные источники данных для восходящих и нисходящих свечей.

    Args:
        df (pd.DataFrame): Исходный датафрейм с данными. Должен содержать столбцы 'open', 'close'.

    Returns:
        Tuple[pd.DataFrame, ColumnDataSource, ColumnDataSource, ColumnDataSource]: Кортеж, содержащий:
            - Обработанный датафрейм с дополнительными столбцами.
            - ColumnDataSource для восходящих свечей.
            - ColumnDataSource для нисходящих свечей.
            - ColumnDataSource со всеми данными.

    Note:
        Функция создает следующие дополнительные столбцы в датафрейме:
        - 'middle': среднее значение между 'open' и 'close'.
        - 'height_inc': высота восходящей свечи.
        - 'height_dec': высота нисходящей свечи.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'open': [10, 12, 9], 'close': [11, 10, 11]})
        >>> df, inc_source, dec_source, all_source = create_data_sources(df)
    """
    df = df.copy()

    # Вычисление дополнительных данных для свечей
    df['middle'] = (df['open'] + df['close']) / 2
    df['height_inc'] = df['close'] - df['open']
    df['height_dec'] = df['open'] - df['close']

    # Разделение данных на восходящие и нисходящие свечи
    inc = df['close'] > df['open']
    dec = df['open'] > df['close']

    # Создание источников данных
    df_inc = ColumnDataSource(df[inc])
    df_dec = ColumnDataSource(df[dec])
    df_source = ColumnDataSource(df)

    return df, df_inc, df_dec, df_source