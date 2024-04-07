from fastapi import APIRouter


router = APIRouter(tags=["Стажировка"])


"""
Задание_1. Удаление дублей
    Реализуйте функцию соответствующую следующему описанию:
    На вход подаётся массив слов зависимых от регистра, для которых необходимо произвести
    фильтрацию на основании дублей слов, если в списке найден дубль по регистру, то все
    подобные слова вне зависимости от регистра исключаются.
    На выходе должны получить уникальный список слов в нижнем регистре.

    Список слов для примера: ['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт', 'Дядя', 'Дядя', 'Дядя']
    Ожидаемый результат: ['папа','брат']
"""
@router.post("/find_in_different_registers", description="Задание_1. Удаление дублей")
async def find_in_different_registers(words: list[str]) -> list[str]:
    """Описание."""
    result = words
    for word in words:
        if words.count(word) > 1:
            result = list((w.lower() for w in result if w.lower() != word.lower()))
    result = list(set(result))
    return result
