"""
Модуль Владосик
"""


import os
import time
import copy
import psutil
import psycopg2
import functools
import numpy as np
import pandas as pd
import multiprocessing
import matplotlib.pyplot as plt


from itertools import chain
from tqdm.notebook import tqdm
from warnings import filterwarnings
from abc import ABC, abstractmethod
from typing import List, Type, Union, Any





@lst_to_array
def get_class_answers(y_true, y_pred, n_classes=None, start_from_class=1):
    """Вычисляет количество True Positive, False Positive и False Negative для каждого класса.

    Обрабатывает как бинарную, так и многоклассовую классификацию. Для многоклассовой
    классификации предполагается, что y_pred содержит вероятности или логиты,
    и метка класса определяется через argmax. Для бинарной - по порогу 0.5.

    Args:
        y_true: Истинные метки классов (1D массив).
        y_pred: Предсказанные метки или вероятности/логиты.
                Для бинарной классификации - 1D массив вероятностей (> 0.5 считается классом 1).
                Для многоклассовой - 2D массив формы (n_samples, n_classes) с вероятностями/логитами.
        n_classes: Общее количество классов. Если None, определяется по уникальным значениям в y_true.
                   Важно указать для многоклассовой классификации, если y_pred - 2D массив.
        start_from_class: Индекс класса, с которого начинать расчет (включительно).
                          Полезно, если класс 0 является фоном и его не нужно учитывать.

    Returns:
        Кортеж из трех списков:
        - tp_list: Список True Positives для каждого класса (начиная со start_from_class).
        - fp_list: Список False Positives для каждого класса.
        - fn_list: Список False Negatives для каждого класса.
    """
    
    if not n_classes:
        n_classes = len(np.unique(y_true))
    if n_classes > 2:
        y_pred = y_pred.argmax(axis=1)
    else:
        y_pred = y_pred > 0.5
    tp_list = []
    fp_list = []
    fn_list = []
    for i in range(start_from_class, n_classes):
        tp = ((y_pred == i) & (y_true == i)).sum()
        fp = ((y_pred == i) & (y_true != i)).sum()
        fn = ((y_pred != i) & (y_true == i)).sum()
        tp_list.append(tp)
        fp_list.append(fp)
        fn_list.append(fn)
    return tp_list, fp_list, fn_list