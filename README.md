# Учебный инструмент командной строки

## Описание

Инструмент командной строки разработан для преобразования текста из входного формата TOML в выходной формат учебного конфигурационного языка. Программа поддерживает проверку синтаксических ошибок с выводом сообщений об ошибках.

## Особенности

1. **Комментарии:**
   - Однострочные комментарии начинаются с символа `\`:
     ```
     \ Это однострочный комментарий
     ```
   - Многострочные комментарии заключены в `|#` и `#|`:
     ```
     |#
     Это многострочный
     комментарий
     #|
     ```

2. **Словари:**
   - Словари записываются в фигурных скобках:
     ```
     {
       имя : значение;
       имя : значение;
     }
     ```

3. **Имена:**
   - Имена состоят из строчных латинских букв `[a-z]+`.

4. **Значения:**
   - Числа.
   - Вложенные словари.

5. **Объявление констант:**
   - Константа объявляется с помощью ключевого слова `is`:
     ```
     имя is значение
     ```

6. **Вычисление констант:**
   - Константное выражение вычисляется с использованием записи `.[имя].`:
     ```
     .[имя].
     ```