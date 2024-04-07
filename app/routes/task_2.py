from typing import Annotated

from fastapi import APIRouter, Body

from app.core import convert_arabic_to_roman, convert_roman_to_arabic
from app.models import ConverterResponse

router = APIRouter(tags=["Стажировка"])

"""
Задание_2. Конвертер
    1. Реализовать функции convert_arabic_to_roman() и convert_roman_to_arabic() из пакета app.core
    2. Написать логику и проверки для вводимых данных. Учитывать, что если арабское число выходит за пределы 
    от 1 до 3999, то возвращать "не поддерживается"
    3. Запустить приложение и проверить результат через swagger
"""


@router.post("/converter", description="Задание_2. Конвертер")
async def convert_number(number: Annotated[int | str, Body()]) -> str | ConverterResponse:
    """
    Принимает арабское или римское число.
    Конвертирует его в римское или арабское соответственно.
    Возвращает первоначальное и полученное числа в виде json:
    {
        "arabic": 10,
        "roman": "X"
    }
    """
    print(type(number))
    dict_arabic_roman = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
                         'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
                         'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}

    converter_response = ConverterResponse(roman="", arabic=1)
    if type(number) is str:
        try:
            arabic = 0
            i = 0
            while i <= len(number) - 1:
                if i != len(number) - 1 and dict_arabic_roman.get(number[i]) < dict_arabic_roman[number[i + 1]]:
                    arabic += dict_arabic_roman.get(number[i] + number[i + 1])
                    i += 2
                else:
                    arabic += dict_arabic_roman.get(number[i])
                    i += 1

            converter_response = ConverterResponse(roman=number, arabic=arabic)
        except TypeError:
            return 'Неправильно введенно римское число'
    elif number <= 3999:
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
        converter_response = ConverterResponse(roman=roman, arabic=number)
    else:
        return "Не поддерживается"
    return converter_response
