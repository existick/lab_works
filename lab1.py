import time  # модуль времени: паузы time.sleep()
import os  # модуль ОС: очистка консоли os.system("clear")

# Цвета, которые используются в нескольких заданиях
RESET = "\033[0m"       # сброс цвета
WHITE = "\033[107m"     # ярко-белый фон (флаг, узор, шкала)
GREEN_BG = "\033[42m"   # зелёный фон (диаграмма, график)


# Задание 1. Флаг страны
def print_finland_flag():
    BLUE = "\033[44m"  # синий фон
    print("=== Задание 1: флаг Финляндии ===")  # заголовок
    for r in range(11):  # 11 строк флага
        line = ""  # здесь собираем одну строку флага
        for c in range(18):  # 18 столбцов флага
            in_cross = 4 <= r <= 6 or 5 <= c <= 6  # ячейка в горизонтальной (строки 4-6) или вертикальной (столбцы 5-6) перекладине
            line += (BLUE if in_cross else WHITE) + "  "  # синяя ячейка в кресте, иначе белая (ячейка = два пробела)
        print(line + RESET)  # печатаем строку, сбрасываем цвет
    print()  # пустая строка


print_finland_flag()  # выводим флаг


# Задание 2. Узор
def print_pattern_i():
    CIRCLES = 2  # сколько кругов в строке
    RADIUS = 4  # радиус круга в ячейках
    BLACK = "\033[40m"  # чёрный фон (внутри круга)
    size = 2 * RADIUS + 1  # ширина и высота одного круга в ячейках
    print("=== Задание 2: узор (вариант i) ===")  # заголовок
    for row in range(size):  # цикл по строкам узора
        line = ""  # здесь собираем одну строку узора
        for _ in range(CIRCLES):  # цикл по кругам
            for col in range(size):  # цикл по ячейкам одного круга
                inside = (col - RADIUS) ** 2 + (row - RADIUS) ** 2 <= (RADIUS + 0.5) ** 2  # ячейка внутри круга (уравнение окружности)
                line += (BLACK if inside else WHITE) + "  "  # чёрная ячейка внутри круга, иначе белая
        print(line + RESET)  # печатаем строку, сбрасываем цвет
    print()  # пустая строка


print_pattern_i()  # выводим узор


# Задание 3. Анимация
def animate():
    PAUSE_BEFORE = 3  # пауза перед анимацией, сек
    FRAME_DELAY = 1  # сколько секунд виден один кадр
    ROW = 5  # строка экрана, в которой рисуется шкала
    BAR_WIDTH = 40  # длина шкалы в символах
    PERCENTS = [25, 50, 75, 100]  # проценты по кадрам (4 числа = 4 кадра)

    time.sleep(PAUSE_BEFORE)  # ждём, чтобы успеть рассмотреть флаг и узор
    print("\033[?25l", end="")  # прячем курсор
    frame_number = 1  # номер кадра для подписи
    for percent in PERCENTS:  # один проход цикла = один кадр
        os.system("clear")  # очищаем консоль
        print("\033[2J\033[3J\033[H", end="")  # стираем экран и историю прокрутки, курсор в начало
        print("Кадр " + str(frame_number) + " из " + str(len(PERCENTS)))  # подпись кадра
        filled = BAR_WIDTH * percent // 100  # сколько символов шкалы закрасить
        bar = "[" + WHITE + " " * filled + RESET + " " * (BAR_WIDTH - filled) + "]"  # рамка, белая часть, пустая часть, рамка
        print("\033[" + str(ROW) + ";1H" + bar + " \033[97m" + str(percent) + "%" + RESET)  # курсор в строку ROW, шкала и проценты белым цветом
        time.sleep(FRAME_DELAY)  # держим кадр на экране
        frame_number += 1  # следующий кадр
    print("\033[" + str(ROW + 2) + ";1H\033[?25hЗагрузка завершена")  # курсор под шкалу, показываем курсор, сообщение
    print()  # пустая строка


animate()  # запускаем анимацию


# Задание 4. Диаграмма
def print_percentage_diagram():
    FILE_NAME = "sequence.txt"  # имя файла с числами
    A_MIN, A_MAX = 5, 10  # группа A: числа от 5 до 10
    B_MIN, B_MAX = -10, -5  # группа B: числа от -10 до -5
    BAR_WIDTH = 40  # длина диаграммы в символах
    RED_BG = "\033[41m"  # красный фон (группа B)

    print("=== Задание 4: диаграмма по sequence.txt ===")  # заголовок
    file = open(FILE_NAME)  # открываем файл для чтения
    count_a = 0  # сколько чисел в группе A
    count_b = 0  # сколько чисел в группе B
    for line in file:  # по строкам файла (одно число в строке)
        number = float(line)  # переводим строку в число
        if A_MIN <= number <= A_MAX:  # число в группе A?
            count_a += 1  # да: увеличиваем счётчик A
        elif B_MIN <= number <= B_MAX:  # иначе число в группе B?
            count_b += 1  # да: увеличиваем счётчик B
    file.close()  # закрываем файл; остальные числа отброшены

    percent_a = count_a * 100 / (count_a + count_b)  # доля A, сумма количеств = 100%
    percent_b = 100 - percent_a  # доля B: остаток до 100%
    len_a = round(BAR_WIDTH * percent_a / 100)  # длина зелёной части в символах
    print(GREEN_BG + " " * len_a + RED_BG + " " * (BAR_WIDTH - len_a) + RESET)  # диаграмма: зелёная часть + красная часть
    print()  # пустая строка
    print(GREEN_BG + "  " + RESET + " числа от " + str(A_MIN) + " до " + str(A_MAX) + ": " + str(count_a) + " шт. - " + str(round(percent_a, 2)) + "%")  # подпись A
    print(RED_BG + "  " + RESET + " числа от " + str(B_MIN) + " до " + str(B_MAX) + ": " + str(count_b) + " шт. - " + str(round(percent_b, 2)) + "%")  # подпись B
    print()  # пустая строка


print_percentage_diagram()  # выводим диаграмму


# Дополнительное задание. График
def build_function_graph():
    X_MAX = 16  # правая граница по x
    height = int(X_MAX / 2) + 1  # число строк: y от 0 до X_MAX / 2 (при X_MAX = 16 это 9 строк)
    picture = ""  # здесь собираем всю картинку графика
    for r in range(height):  # цикл по строкам (r = 0 - верхняя)
        for c in range(X_MAX + 1):  # цикл по столбцам (c - это x)
            if c == 0 or r == height - 1:  # левый столбец или нижняя строка
                picture += "\033[100m  " + RESET  # ячейка оси (серый фон)
            elif height - 1 - r == int(c / 2 + 0.5):  # уровень строки равен y = x / 2, округлённому до целого
                picture += GREEN_BG + "  " + RESET  # ячейка линии графика
            else:
                picture += "  "  # пустая ячейка
        picture += "\n"  # конец строки картинки
    print("=== Допзадание: график y = x/2 ===")  # заголовок
    print(picture)  # выводим картинку одним print


build_function_graph()  # выводим график