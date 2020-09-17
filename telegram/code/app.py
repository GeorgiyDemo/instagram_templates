import os
import time
import base64
from io import BytesIO

import requests
import telegram
from telegram.error import NetworkError, Unauthorized


class TelegramCli:
    """Telegram CLI"""

    def __init__(self, token, proxy):

        self.buffer_dict = {}
        self.update_id = None

        if proxy is not None and proxy != "":
            request = telegram.utils.request.Request(proxy_url=proxy)
            self.bot = telegram.Bot(token, request=request)
        else:
            self.bot = telegram.Bot(token)
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

        while True:
            try:
                self.handler()
            except NetworkError:
                time.sleep(1)
            except Unauthorized:
                self.update_id += 1

    def handler(self):

        for update in self.bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1

            user_id = update.message.chat.id
            if update.message.text is None:
                user_msg = ""
            else:
                user_msg = update.message.text

            # Если это начало работы с ботом
            if user_msg == "/start":
                update.message.reply_text(
                    "Привет, пришли мне изображение в виде документа и я сделаю шаблон для instagram"
                )

            # Если пользователь прислал файл
            elif update.message.document is not None:
                file_data = update.message.document
                file_name = file_data["file_name"]

                new_file = self.bot.getFile(file_data["file_id"])
                file_source = "./images/{}".format(file_name)
                new_file.download(file_source)

                self.buffer_dict[user_id] = file_source
                update.message.reply_text(
                    'Теперь отправь параматры в следующем виде:\n "Заголовок" "подзаголовок" "код_страны"'
                )

            # Если пользователь отправил сообщение и он есть в buffer_dict, то это параматры для файла
            elif user_msg != "" and user_id in self.buffer_dict:

                file_args = list(
                    map(
                        lambda x: x.replace('"', ""),
                        [value for value in user_msg.split('" "')],
                    )
                )
                if len(file_args) == 3:
                    title, subtitle, flag = file_args

                    print(self.buffer_dict[user_id])
                    with open(self.buffer_dict[user_id], "rb") as file:
                        r = requests.post(
                            "http://flask:5000/create_image",
                            data={"title": title, "subtitle": subtitle, "flag": flag},
                            files={"image": file},
                        ).json()

                    if not r["exception"]:
                        imgdata = BytesIO(base64.b64decode(r["result"]))
                        imgdata.name = "image.jpg"
                        imgdata.seek(0)
                        self.bot.send_document(
                            chat_id=update.message.chat_id, document=imgdata
                        )

                    else:
                        update.message.reply_text("Flask возвратил ошибку")

                    del self.buffer_dict[user_id]

                else:
                    update.message.reply_text("Некорректный ввод параметров")


def main():

    tg_token = os.getenv("TELEGRAM_TOKEN", None)
    tg_proxy = os.getenv("TELEGRAM_PROXY", None)
    TelegramCli(tg_token, tg_proxy)


if __name__ == "__main__":
    main()
