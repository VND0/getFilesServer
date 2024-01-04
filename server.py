from flask import Flask, request, make_response


class Checker:
    """
    Класс реализует проверку входящего файла на отсутствие попыток вредоносных воздействий на сервер.
    Проверки:
        1. По имени:
            - белый список расширений;
            - изменение каталога.
    """

    allowed_extensions = ("txt", "docx", "doc", "ppt", "pptx", "rtf", "xls", "xslx",
                          "pdf", "jpg", "jpeg", "png", "bmp", "heic")
    forbidden_patterns = ("../", "/..", "\b", "\\b")

    def __check_file_by_filename(self, filename: str) -> bool:
        """
            Осуществляет проверку имени файла, а именно:
                1. Предотвращает попытку изменения каталога.
                2. Осуществляет фильтрацию по расширению в соответствии с "белым списком".

            :param filename: Имя файла.
            :return: True: проверка пройдена; False: проверка не пройдена.
        """

        for pattern in self.forbidden_patterns:
            if pattern in filename:
                return False

        dot_rindex = filename.rindex(".")
        extension = filename[dot_rindex + 1:].lower()
        if extension not in self.allowed_extensions:
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


class Server:
    download_dir = "."
    max_size_bytes = 100 * 1024 * 1024
    checker = Checker()

    def __init__(self, name_: str):
        self.app = Flask(name_)
        self.__upload_handler = self.__init_route_to_upload()

    def config_server(self) -> None:
        self.app.config["UPLOAD_FOLDER"] = self.download_dir
        self.app.config["MAX_CONTENT_LENGTH"] = self.max_size_bytes

    def __init_route_to_upload(self) -> ():
        @self.app.route("/send", methods=["GET", "POST"])
        def get_sent_file():
            f = request.files["file"]
            filename = f.filename
            if self.checker.complex_check_file(filename):
                f.save(filename)
                resp = make_response({"message": f"Saved as {filename} successfully."}, 200)
                resp.headers["Content-Type"] = "application/json"
                return resp
            else:
                resp = make_response({"message": "File is forbidden."}, 403)
                resp.headers["Content-Type"] = "application/json"
                return resp

        return get_sent_file


if __name__ == '__main__':
    srv = Server(__name__)
    app = srv.app

    app.run(debug=True, port=8889)
