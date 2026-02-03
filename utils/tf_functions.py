import random
import numpy as np
import pandas as pd
import re
from tqdm import tqdm


#===Функция предобработки текста
def func_preProcess(text_loc):
    SPECIAL_CHARS = r"([^a-z0-9\s])\1+"
    flags_ignorecase_multiline = re.IGNORECASE | re.MULTILINE
    # Замена подряд идущих специальных символов на пробел.
    res_text = re.sub(SPECIAL_CHARS, " ", text_loc, flags=flags_ignorecase_multiline)

    # Сжатие текста в одну строку путем  замены всех
    # лишних пробелов, \t, \n, \r и т.д. на один пробел.
    return re.sub(r"\s+", " ", res_text).strip()


#===Функция преобразования входного текста в тензор
def tensor_create(text_loc):
    res_parsed_data = []
    preprocessed_text = func_preProcess(text_loc)
    # Преобразование обработанный текст из документов в DataFrame.
    col_names = ["Текст"]
    res_parsed_data.append([preprocessed_text])
    parsed_dataframe = pd.DataFrame(res_parsed_data, columns=col_names)

    return parsed_dataframe






#===Функция загрузки модели в систему
def load_model(model_loc):
    res = model_loc
    return res

#===Функция определения весов категорий документов
def predict(model_loc, text_arr_loc):
    n = 100  # кол-во экспериментов

    res_weights = np.array([0.0, 0.0, 0.0, 0.0,])
    for i in range(n):
        nums = [random.random() for _ in range(4)]
        total = sum(nums)
        normalized_nums = [n / total for n in nums]
        res_weights = np.add(res_weights,normalized_nums)
    res_weights =  [pp / n for pp in res_weights]
    return normalized_nums


