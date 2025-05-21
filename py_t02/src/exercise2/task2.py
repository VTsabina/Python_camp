import asyncio
import aiohttp
import aiofiles
import os
from prettytable import PrettyTable


class ImageManager:
    def __init__(self, path, image_url):
        self.path = path
        self.url = image_url

    async def download_image(self, session, res):
        try:
            async with session.get(self.url) as response:
                response.raise_for_status()
                filename = os.path.join(self.path, os.path.basename(self.url))
                async with aiofiles.open(filename, 'wb') as f:
                    await f.write(await response.read())
            print(f"Успешно: {self.url}")
            res[self.url] = "Успех"
            return
        except Exception as e:
            res[self.url] = "Ошибка"
            print(f"Ошибка при загрузке {self.url} : {e}")
            return


def get_path():
    exit = 0
    while not exit:
        input_path = input("Введите путь для сохранения:\n")
        if os.path.exists(input_path) and os.path.isdir(input_path):
            if os.access(input_path, os.W_OK):
                exit = 1
            else:
                print("Доступ к директории запрещен. Попробуйте снова.")
        else:
            print("Выбранной вами папки не существует.")
    return input_path


def print_results(res):
    table = PrettyTable()
    table.field_names = ["Ссылка", "Статус"]
    for img in res.keys():
        table.add_row([img, res[img]])
    print(table)


async def main():
    path = get_path()
    res = {}

    async with aiohttp.ClientSession() as session:
        tasks = []
        print("Введите ссылку на изображение (Enter для завершения):")
        while True:
            url = input()
            if not url:
                break
            manager = ImageManager(path, url)

            task = asyncio.ensure_future(
                manager.download_image(session, res))
            tasks.append(task)

        if tasks:
            while tasks:
                print(f"Ожидание скачивания изображений...")
                await asyncio.wait(tasks)
                tasks = []

    print_results(res)


if __name__ == "__main__":
    asyncio.run(main())
