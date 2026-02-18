import re
import tensorflow as tf
from functools import lru_cache
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json

# === Функция предобработки текста
def func_preProcess(text_loc: str) -> str:
    SPECIAL_CHARS = r"([^a-z0-9\s])\1+"
    flags_ignorecase_multiline = re.IGNORECASE | re.MULTILINE
    res_text = re.sub(SPECIAL_CHARS, " ", text_loc, flags=flags_ignorecase_multiline)
    return re.sub(r"\s+", " ", res_text).strip()

# === Преобразование текста в вход для модели
def tensor_create(text_loc: str):
    preprocessed = func_preProcess(text_loc)
    # ВАЖНО: большинство Keras-текстовых моделей ожидают список/тензор строк
    return tf.constant([preprocessed])  # shape=(1,)

# === Загрузка модели (кэшируем, чтобы не грузить каждый раз)
@lru_cache(maxsize=2)
def load_model(model_path: str):
    return tf.keras.models.load_model(model_path)

MAX_LEN = 380
POS_DIM = 17

def func_preProcess(text_loc: str) -> str:
    SPECIAL_CHARS = r"([^a-z0-9\s])\1+"
    flags = re.IGNORECASE | re.MULTILINE
    res_text = re.sub(SPECIAL_CHARS, " ", text_loc, flags=flags)
    return re.sub(r"\s+", " ", res_text).strip()

def load_tokenizer(path="tokenizer.json"):
    with open(path, "r", encoding="utf-8") as f:
        return tokenizer_from_json(f.read())

TOKENIZER = load_tokenizer("tokenizer.json")

def make_input_text(text_loc: str):
    text = func_preProcess(text_loc)
    seq = TOKENIZER.texts_to_sequences([text])
    x = pad_sequences(seq, maxlen=MAX_LEN, padding="post", truncating="post")
    return x.astype("int32")

def make_input_pos(text_loc: str):
    # пока заглушка: нулевой вектор признаков (1, 17)
    return np.zeros((1, POS_DIM), dtype="float32")

def predict(model, x_text, x_pos):
    return model.predict([x_text, x_pos], verbose=0)
