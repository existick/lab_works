from csv import reader  # Импортируем reader для чтения CSV-файла
import random  # Импортируем модуль для случайного выбора книг
import xml.dom.minidom as minidom  # Импортируем модуль для чтения XML
from collections import Counter  # Импортируем Counter для подсчёта выдач книг


# Индексы столбцов в books.csv, нумерация начинается с нуля
COL_TITLE, COL_AUTHOR, COL_DATE = 1, 3, 6  # Столбцы с названием, автором и датой
COL_PRICE, COL_ISSUES, COL_TAGS = 7, 8, 12  # Столбцы с ценой, выдачами и тегами


def open_table():  # Читаем таблицу книг из CSV-файла
    with open('books.csv', encoding='windows-1251') as file:  # Открываем файл в кодировке для русских букв
        return list(reader(file, delimiter=';'))[1:]  # Читаем строки, разделённые точкой с запятой, и пропускаем заголовок


def task_long_titles(table):  # Считаем книги с названием длиннее 30 символов
    count = sum(len(row[COL_TITLE]) > 30 for row in table)  # Складываем результаты проверок
    print('=== Задание 1: длинные названия ===')  # Выводим заголовок задания
    print(f'Записей с названием длиннее 30 символов: {count}\n')  # Выводим количество книг


def task_search_author(table):  # Ищем книги по автору с ценой от 200 рублей
    print('=== Задание 2: поиск по автору (цена от 200 руб.) ===')  # Выводим заголовок задания
    while True:  # Повторяем поиск, пока пользователь не введёт 0 или пустую строку
        search = input('Введите автора (0 - перейти дальше): ')  # Запрашиваем имя или часть имени автора
        if search in ('0', ''):  # Проверяем, попросил ли пользователь закончить поиск
            break  # Завершаем цикл поиска

        found = 0  # Обнуляем счётчик найденных книг
        for row in table:  # Перебираем все строки таблицы
            price = float(row[COL_PRICE].replace(',', '.'))  # Преобразуем цену из текста в число
            if search.lower() in row[COL_AUTHOR].lower() and price >= 200:  # Ищем автора без учёта регистра и проверяем цену
                print(f'{row[COL_AUTHOR]} | {row[COL_TITLE]} | {price} руб.')  # Выводим автора, название и цену
                found += 1  # Увеличиваем счётчик найденных книг

        if found:  # Проверяем, нашлись ли подходящие книги
            print(f'Найдено записей: {found}')  # Выводим количество найденных книг
        else:  # Выполняем, если подходящих книг нет
            print('Ничего не найдено.')  # Сообщаем, что совпадений нет


def task_links(table):  # Создаём библиографические ссылки
    rows = random.sample([row for row in table if row[COL_AUTHOR].strip()], 20)  # Выбираем 20 книг с указанным автором без повторов

    with open('links.txt', 'w', encoding='utf-8') as file:  # Открываем файл для записи ссылок
        for number, row in enumerate(rows, 1):  # Перебираем книги и нумеруем их начиная с 1
            year = row[COL_DATE].split()[0].split('.')[-1]  # Извлекаем год из даты вида «15.10.2021 9:22»
            file.write(f'{number}. {row[COL_AUTHOR]}. {row[COL_TITLE]} - {year}\n')  # Записываем ссылку в файл

    print('=== Задание 3: библиографические ссылки ===')  # Выводим заголовок задания
    print('Ссылки сохранены в файл links.txt\n')  # Сообщаем, куда сохранены ссылки


def task_xml():  # Читаем цифровые и буквенные коды валют из XML
    currencies = minidom.parse('currency.xml').getElementsByTagName('Valute')  # Находим все элементы с валютами

    num_codes = []  # Создаём список цифровых кодов валют
    char_codes = []  # Создаём список буквенных кодов валют
    for node in currencies:  # Перебираем все валюты в XML
        num_codes.append(int(node.getElementsByTagName('NumCode')[0].firstChild.data))  # Читаем NumCode и преобразуем его в число
        char_codes.append(node.getElementsByTagName('CharCode')[0].firstChild.data)  # Читаем CharCode и сохраняем его как текст

    print('=== Задание 4: currency.xml ===')  # Выводим заголовок задания
    print(f'Список NumCode: {num_codes}')  # Выводим цифровые коды валют
    print(f'Список CharCode: {char_codes}\n')  # Выводим буквенные коды валют


def extra_tags(table):  # Собираем все теги без повторений
    tags = sorted({  # Создаём множество уникальных тегов и сортируем его
        tag.strip()  # Убираем пробелы по краям тега
        for row in table  # Перебираем строки таблицы
        for tag in row[COL_TAGS].split('#')  # Разделяем теги по символу #
        if tag.strip()  # Пропускаем пустые части
    })  # Получаем отсортированный список тегов

    print('=== Допзадание 1: теги без повторений ===')  # Выводим заголовок задания
    print(f'Всего тегов: {len(tags)}')  # Выводим количество уникальных тегов
    print(', '.join(tags), '\n')  # Выводим теги через запятую


def extra_popular(table):  # объявляем функцию популярных книг

    TOP = 20  # сколько книг показать

    issues = {}  # словарь {"автор | название": сколько раз книгу выдавали}
    for row in table:  # цикл по всем записям
        name = f'{row[COL_AUTHOR]} | {row[COL_TITLE]}'  # "имя" книги: автор и название вместе
        count = int(row[COL_ISSUES])  # сколько раз выдавали этот экземпляр (текст -> целое число)
        if name in issues:  # эта книга уже есть в словаре?
            issues[name] += count  # да: прибавляем выдачи к уже посчитанным
        else:  # иначе книга встретилась впервые
            issues[name] = count  # записываем её с текущим числом выдач

    pairs = []  # список пар [число выдач, имя книги]
    for name in issues:  # цикл по именам книг в словаре
        pairs.append([issues[name], name])  # кладём пару в список
    pairs.sort(reverse=True)  # сортируем по первому числу от большего к меньшему (reverse=True - в обратном порядке)

    print('=== Допзадание 2: 20 самых популярных книг ===')  # печатаем заголовок
    for i in range(TOP):  # цикл по первым 20 местам, i - от 0 до 19
        print(f'{i + 1}. {pairs[i][1]} | выдач: {pairs[i][0]}')  # номер места, имя книги (элемент 1 пары) и число выдач (элемент 0 пары)
    print()  # пустая строка-отступ


table = open_table()  # Загружаем таблицу из файла
task_long_titles(table)  # Выполняем задание 1
task_search_author(table)  # Выполняем задание 2
task_links(table)  # Выполняем задание 3
task_xml()  # Выполняем задание 4
extra_tags(table)  # Выполняем дополнительное задание 1
extra_popular(table)  # Выполняем дополнительное задание 2
