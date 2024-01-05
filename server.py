from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import uvicorn


class Checker:
    """
    Класс реализует проверку входящего файла на отсутствие попыток вредоносных воздействий на сервер.
    Проверки:
        1. По имени:
            - белый список расширений;
            - изменение каталога.
    """

    __allowed_extensions = ("txt", "docx", "doc", "ppt", "pptx", "rtf", "xls", "xslx",
                          "pdf", "jpg", "jpeg", "png", "bmp", "heic")
    __forbidden_patterns = ("../", "/..", "\b", "\\b")

    def __check_file_by_filename(self, filename: str) -> bool:
        """
            Осуществляет проверку имени файла, а именно:
                1. Предотвращает попытку изменения каталога.
                2. Осуществляет фильтрацию по расширению в соответствии с "белым списком".

            :param filename: Имя файла.
            :return: True: проверка пройдена; False: проверка не пройдена.
        """

        for pattern in self.__forbidden_patterns:
            if pattern in filename:
                return False

        dot_rindex = filename.rindex(".")
        extension = filename[dot_rindex + 1:].lower()
        if extension not in self.__allowed_extensions:
            return False
        else:
            return True

    def complex_check_file(self, filename: str) -> bool:
        """
        Метод, который совмещает все проверки входящего файла и упрощает расширение функционала.

        :param filename: Имя файла.
        :return: True: проверка пройдена; False: проверка не пройдена.
        """

        check_01 = self.__check_file_by_filename(filename)

        return check_01


def main() -> None:
    app = FastAPI()
    checker = Checker()

    @app.post("/upload/")
    async def upload_file(file: UploadFile = File(...)):
        try:
            filename = file.filename
            allowed = checker.complex_check_file(filename)
            if not allowed:
                return JSONResponse(content={"message": f"It is not allowed to upload {filename}"}, status_code=403)
        except Exception as e:
            return JSONResponse(content={"message": f"An error occurred: {e}"}, status_code=500)

        try:
            with open(f"destination\\{file.filename}", "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return JSONResponse(content={"message": "File uploaded successfully"})
        except Exception as e:
            return JSONResponse(content={"message": f"An error occurred: {e}"}, status_code=500)

    uvicorn.run(app)  # On server you should add here host and port.


if __name__ == '__main__':
    main()
