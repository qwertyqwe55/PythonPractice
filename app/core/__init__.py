import csv
import json
import os
import string
import uuid
from abc import ABC, abstractmethod
from io import StringIO, BytesIO
import random
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pandas as pd
from fastapi.exceptions import HTTPException
import numpy as np
from fastapi import UploadFile, File
from app.routes.task_5 import Example
import yaml

def convert_arabic_to_roman(number: int) -> str:
    dict_arabic_roman = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
                         'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
                         'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}

    roman = ""
    arabic = number
    for i in (1000, 100, 10, 1):
        delta = arabic // i * i
        for key, value in dict_arabic_roman.items():
            if value == delta:
                roman += key
                break
            elif delta // value > 0:
                roman += (delta // value) * key
                delta %= value
            elif delta // i == 0:
                break
        arabic = arabic % i
    return roman


def convert_roman_to_arabic(number: str) -> int:
    dict_arabic_roman = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
                         'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
                         'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    arabic = 0
    i = 0
    while i <= len(number) - 1:
        if i != len(number) - 1 and dict_arabic_roman.get(number[i]) < dict_arabic_roman[number[i + 1]]:
            arabic += dict_arabic_roman.get(number[i] + number[i + 1])
            i += 2
        else:
            arabic += dict_arabic_roman.get(number[i])
            i += 1
    return arabic


def average_age_by_position(file) -> dict:
    try:
        contents = file.file.read()
        if not contents.decode('utf-8').find('Имя,Возраст,Должность') > -1:
            raise HTTPException(status_code=400, detail="Неправильное название столбцов")
        buffer = BytesIO(contents)
        data = pd.read_csv(buffer, delimiter=',', header=0,
                           names=['name', 'age', 'job'])

        buffer.close()

        # Проверка на валидные данные
        if ("" not in tuple(data["name"])
                and ("" not in tuple(data["age"]))
                and not np.all(data["age"].apply(lambda x: isinstance(x, int) and x > 0))
                and "" not in tuple(data["job"])):
            raise HTTPException(status_code=400, detail="Неккоректные данные")

        # Создаем уникальный набор должностей
        jobs = set(list(data.job))
        # Словарь с должностью и средним возрастом (равным 0 при инициализации)
        jobs = {job: 0 for job in jobs}

        # Считаем средний возраст по каждой должности
        for job in jobs.keys():
            sum = 0
            count = 0
            for j, age in zip(list(data.job), list(data.age)):
                if j == job:
                    sum += age
                    count += 1
            jobs[job] = sum / count


    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file пустой")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Неправильный формат файла")
    return jobs


"""
Задание_6.
Дан класс DataGenerator, который имеет два метода: generate(), to_file()
Метод generate генерирует данные формата list[list[int, str, float]] и записывает результат в
переменную класса data
Метод to_file сохраняет значение переменной generated_data по пути path c помощью метода
write, классов JSONWritter, CSVWritter, YAMLWritter.

Допишите реализацию методов и классов.
"""


class BaseWriter(ABC):
    """Абстрактный класс с методом write для генерации файла"""

    @abstractmethod
    def write(self, path: str, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в json формате"""

    """Ваша реализация"""

    def write(self, path: str, data: list[list[int, str, float]]) -> dict:
        data_json = {}
        for i in range(0, len(data)):
            data_json[i] = []
            data_json[i].append({
                'int': data[i][0],
                'string': data[i][1],
                'float': data[i][2]
            })
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
        return data_json


class CSVWriter(BaseWriter):
    def write(self, path: str, data: list[list[int, str, float]]) -> list:
        data_csv= [["int", "string", "float"]]
        for i in range(0, len(data)):
            data_csv.append(data[i])

        print(data_csv)
        with open(path, 'w',newline='') as myFile:
            writer = csv.writer(myFile)
            writer.writerows(data_csv)
        return data_csv


class YAMLWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате"""

    """Ваша реализация"""

    def write(self, path: str, data: list[list[int, str, float]]) -> dict:
        data_yaml = {'data' : []}
        with open(path, 'w') as outfile:
            for i in range(0, len(data)):
                temp_dict = {}
                temp_dict['int'] = data[i][0]
                temp_dict['string'] = data[i][1]
                temp_dict['float'] = data[i][2]
                data_yaml['data'].append(temp_dict)
            yaml.dump(data_yaml, outfile, default_flow_style=False)
        return data_yaml


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id = None

    def generate(self, matrix_size) -> None:
        """Генерирует матрицу данных заданного размера."""

        data: list[list[int, str, float]] = []
        """Ваша реализация
        Происходит создание рандомных данным в заданной матрице"""

        for i in range(0, matrix_size):
            data.append([random.randint(1, 1000),
                         ''.join(random.sample(string.ascii_lowercase, 10)),
                         random.uniform(1, 10)])
        self.data = data

    # writer
    def to_file(self, path: str, writer: BaseWriter):
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """
        """Ваша реализация"""

        # Проверка что данные есть
        if len(self.data) != 0:
            # Создаем директорию если нужно
            path_dict = path.replace(os.path.basename(path).split('/')[-1], "")
            if not os.path.isdir(path_dict):
                os.mkdir(path_dict)

            # Подключаемся к нашей бд и добавляем в нее сгенерированный файл
            engine = create_engine("sqlite:///test.db")
            writer.write(path, self.data)
            f = UploadFile(File(...))
            f.file = open(path, "rb")
            f.filename = os.path.basename(path).split('/')[-1]
            example = Example(file=f)
            with Session(engine) as session:
                session.add(example)
                session.commit()
                return example.id
        else:
            raise HTTPException(status_code=400, detail="Нет данных")
