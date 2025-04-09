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
from bokeh.layouts import column, row
from bokeh.models import Span, LabelSet, HoverTool, Slider, DatePicker, Toggle, CrosshairTool, FreehandDrawTool
from bokeh.models.callbacks import CustomJS
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, show, ColumnDataSource


def customize_plot_styles(p: figure) -> None:
    """


    Настраивает стили графика Bokeh для улучшения его внешнего вида.

    Эта функция применяет ряд стилистических изменений к объекту Figure из Bokeh,
    включая цвета фона, осей, сетки, а также настройки отображения меток и линий.

    Args:
        p (bokeh.plotting.Figure): Объект Figure из Bokeh, который нужно настроить.

    Returns:
        None: Функция изменяет переданный объект Figure и ничего не возвращает.

    Note:
        Эта функция модифицирует переданный объект Figure напрямую.
        Основные изменения включают:
        - Установку темного фона (#181c27)
        - Настройку цветов и стилей осей
        - Настройку сетки (пунктирные линии, прозрачность)
        - Удаление линий тиков
        - Автоскрытие панели инструментов
    """
    # Настройка фона
    p.background_fill_color = "#181c27"
    p.background_fill_alpha = 1
    p.border_fill_color = "#181c27"

    # Настройка оси X
    p.xaxis.major_label_orientation = "horizontal"
    p.xaxis.axis_label_text_color = "#b2b5be"
    p.xaxis.major_label_text_color = "#b2b5be"
    p.xaxis.axis_line_width = 1.0
    p.xaxis.axis_line_color = "#2a2e39"
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None  # Убрать линии тиков по оси X

    # Настройка оси Y
    p.yaxis.axis_label_text_color = "#b2b5be"
    p.yaxis.major_label_text_color = "#b2b5be"
    p.yaxis.axis_line_width = 1.0
    p.yaxis.axis_line_color = "#2a2e39"
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None  # Убрать линии тиков по оси Y

    # Настройка сетки
    p.grid.grid_line_color = "#2a2e39"
    p.outline_line_color = "#2a2e39"
    p.xgrid.grid_line_dash = [2, 2]
    p.ygrid.grid_line_dash = [2, 2]
    p.xgrid.grid_line_alpha = 0
    p.ygrid.grid_line_alpha = 0

    # Дополнительные настройки
    p.toolbar.autohide = True