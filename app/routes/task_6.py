import uuid

import requests as requests
from fastapi import APIRouter

from app.core import DataGenerator, JSONWriter, YAMLWriter, CSVWriter
from app.models import GeneratedFile

router = APIRouter(tags=["API для хранения файлов"])

count = 0

"""
Задание_6. 

Изучите следущие классы в модуле app.core: BaseWriter, DataGenerator

API должно принимать json, по типу:
{
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
}
В ответ на удачную генерацию файла должен приходить id для скачивания.

Добавьте реализацию методов класса DataGenerator.
Добавьте аннотации типов и (если требуется) модели в модуль app.models.

(Подумать, как переисползовать код из задания 5)
"""

@router.post("/generate_file", description="Задание_6. Конвертер")
async def generate_file(file:GeneratedFile):
    """Описание."""

    data = DataGenerator()
    data.generate(10)
    file_id : int
    file_id = 0
    data.generate(file.matrix_size)
    unique_filename = str(uuid.uuid4())
    path = './generated_files'
    path = path + '/' + unique_filename

    if file.file_type == 'json':
        file_id = data.to_file(path + '.json', JSONWriter())
    elif file.file_type == 'yaml':
        file_id = data.to_file(path + '.yaml', YAMLWriter())
    elif file.file_type == 'csv':
        file_id = data.to_file(path + '.csv', CSVWriter())
    return file_id
