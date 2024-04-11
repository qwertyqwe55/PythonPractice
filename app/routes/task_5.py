import os
import zipfile
import aiofiles as aiofiles
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy import Column, Integer, create_engine
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.orm import Session, declarative_base


router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_5. API для хранения файлов

a.	Написать API для добавления(POST) "/upload_file" и скачивания (GET) "/download_file/{id}" файлов. 
В ответ на удачную загрузку файла должен приходить id для скачивания. 
b.	Добавить архивирование к post запросу, то есть файл должен сжиматься и сохраняться в ZIP формате.
с*.Добавить аннотации типов.
"""


""" 1. Создаем базу данных в которой будет хранится загруженные файлы
    2. База данных будет созданана в локальной папке
    3. Загруженные файлы будут хранится в папке tmp( бд служит только длля удобного поиска в этой директории)
"""
Base = declarative_base()
engine = create_engine("sqlite:///test.db")

class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    file = Column(FileType(storage=FileSystemStorage(path="./tmp")))


# Create database and table
Base.metadata.create_all(engine)




@router.post("/upload_file", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile = File(...)) -> int:
    """Описание.
        1. Считываем данные из загруженного файла в локальный файл
        2. Архивируем созданный файл
        3. Добавляем этот файл в file: UploadFile( это нужно для добавления в бд без ошибок)
    """

    # 1. Считываем данные из загруженного файла в локальный файл
    async with aiofiles.open(file.filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    # 2. Архивируем созданный файл
    jungle_zip = zipfile.ZipFile(file.filename +'.zip', 'w')
    jungle_zip.write(file.filename, compress_type=zipfile.ZIP_DEFLATED)
    jungle_zip.close()

    # 3. Добавляем этот файл в file: UploadFile( это нужно для добавления в бд без ошибок)
    file.file = open(file.filename + '.zip', 'rb')
    os.remove(file.filename) # Удаляет локальный файл с данными, так как он нам больше не нужен
    file.filename += '.zip'

    # 4. Добавляется новая запись в бд с загруженным файлом
    example = Example(file=file)

    with Session(engine) as session:
        session.add(example)
        session.commit()
        file.file.close()
        os.remove(file.filename)
        return example.id


@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: int):
    """Описание."""
    with Session(engine) as session:
        results = session.get(Example,file_id)

        return FileResponse(path=results.file, media_type='txt/pdf/mp4/doc/docx/zip',filename=results.file)