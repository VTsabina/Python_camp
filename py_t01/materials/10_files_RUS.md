# Работа с файлами

Файлы являются основным способом хранения и передачи данных между программами и пользователями.
Работа с файлами - взаимодействие с файловой системой для чтения данных из файлов,
записи данных в файлы или выполнения других операций над файлами.

В Python существует ряд встроенных функций и методов, которые облегчают работу с файлами.

## Основные операции

### Открытие

Для начала работы с файлом его необходимо открыть. Это делается с использованием встроенной функции `open()`.
Функция возвращает файловый объект, который используется для выполнения операций чтения или записи.
Второй аргумент в функции `open()` указывает режим открытия файла.
Например, "r" означает чтение, "w" - запись, "a" - добавление, "b" - бинарный режим и так далее.

```python
file = open("example.txt", "r")  # Открытие файла для чтения
```

### Чтение

Для чтения данных из файла используются различные методы, такие как `read()`, `readline()`, `readlines()` и другие.

```python
content = file.read()  # Чтение всего содержимого файла
line = file.readline()  # Чтение одной строки из файла
lines = file.readlines()  # Чтение всех строк файла в список
```

### Запись

Для записи данных в файл используются методы `write()`, `writelines()` и другие.

```python
file = open("example.txt", "w")  # Открытие файла для записи
file.write("Hello, World!")  # Запись строки в файл
```

### Закрытие

После завершения работы с файлом его следует закрыть, чтобы освободить ресурсы.

```python
file.close()
```

Рекомендуется использовать контекстный менеджер `with`, который автоматически закрывает файл после завершения блока кода.

```python
# Файл автоматически закроется после выхода из блока 'with'
with open("example.txt", "r") as file:
    content = file.read()
```

### Работа с бинарными файлами

Если необходимо работать с бинарными данными, можно использовать режим "b" в функции `open()`.

```python
with open("image.jpg", "rb") as binary_file:
    data = binary_file.read()
```
