from installation import *  # Импорт всех функций и данных из файла installation.py
import shutil
import os
import platform


print("Система определена как " + platform.system())

print("Список команд для ввода:"
      "\n1 - crdir [dir name] - Создание папки (с указанием имени)"
      "\n2 - deldir [dir name] - Удаление папки по имени"
      "\n3 - cddir [dir name] - cddir .. - Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх"
      "\n4 - mkfile [filename1 filename2 ...] - Создание пустых файлов с указанием имени"
      "\n5 - wrfile [filename]- Запись текста в файл"
      "\n6 - catfile [filename]- Просмотр содержимого текстового файла"
      "\n7 - rmf [filename1 filename2 ...] - Удаление файлов по имени"
      "\n8 - cpfile [filename folder] - Копирование файлов из одной папки в другую"
      "\n9 - mvfile [filename folder] - Перемещение файлов"
      "\n10 - renamef [filename] [new_filename] - Переименование файлов")

command = input("Введите команду: ")
all_commands = ["crdir", "deldir", "cddir", "mkfile", "wrfile", "catfile", "rmf", "cpfile", "mvfile", "renamef"]
node = os.path.abspath(wd)  # Определяем начальный путь
save_node = node  # Сохраняем этот путь как корневой
path_node = node  # Определяем корневой путь как текущий

# Описание функций для работы с директориями и папками
def crdir(dirname):
    global path_node  # Глобальная переменная, в которой содержится текущий путь
    try:
        print("Создание папки "+dirname)
        os.mkdir(path_node + os.sep + dirname)
    except FileExistsError:
        print('Директория с таким названием уже существует!')

def deldir(dirname):
    global path_node
    try:
        print("Удаление папки "+dirname, path_node + os.sep + dirname)
        os.rmdir(path_node + os.sep + dirname)  # Удаляем директорию
    except OSError:
        ok = input("Папка не пуста, вы уверены, что хотите удалить её? Нажмите Y ")
        if ok == "Y" or ok == "y":
            shutil.rmtree(path_node + os.sep + dirname)  # Принудительно удаляем непустую директорию
        else:
            pass
    except PermissionError:
        print("Папка недоступна для удаления")

def cddir(dirname):
    global path_node
    print("Перемещение в каталог "+dirname)
    os.chdir(path_node + os.sep + dirname)  # Установка новой текущей директории


def mkfile(filename):
    open(filename, "w")  # Создание файла для записи


def wrfile(filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:  # Открытие файла для записи в него текста
            file.write(input())
    except PermissionError:
        print("Это не файл!")

def catfile(filename):
    try:
        with open(filename, 'r') as f:  # Открытие файла для чтения
            data = f.read()
            print(data)
    except PermissionError:
        print("Это не файл!")
    except OSError:
        print("Это не файл!")

def rmf(filename):
    try:
        os.remove(filename)
        print("Удаление файла...")
    except PermissionError:
        print("Это не файл!")

def cpfile(filename, path):
    print("Копирование файла...")
    shutil.copy(filename, path, follow_symlinks=True)  # Копирование файла в другую папку, которая
    # Находится в том же каталоге, что и пользователь


def mvfile(filename, path):
    print("Перемещение файла...")
    if os.path.isfile(filename):  # Проверка, существует ли такой файл
        try:
            shutil.move(filename, path)
        except shutil.Error:
            print("Такой файл уже существует в указанной директории!")
    else:
        print("Такой файл не существует!")


def renamef(filename, new_filename):
    print("Переименование файла...")
    if os.path.isfile(filename):  # Проверка, существует ли такой файл
        shutil.move(filename, new_filename)
    else:
        print("Такой файл не существует!")


def main():
    global command
    global path_node
    global save_node
    while command != 'exit':
        if save_node in path_node:
            lis = command.split()  # Разбиваем введенный текст пользователем для анализа
            if lis[0] in all_commands and len(lis) > 1:  # Если команда является верной (то есть находится в списке команд) и она введена с параметрами
                if lis[0] == "crdir":
                    crdir(lis[1])
                elif lis[0] == "deldir":
                    if os.path.isdir(path_node + os.sep + lis[1]):  # Проверка на существование папки
                        deldir(lis[1])
                elif lis[0] == "cddir":
                    if lis[1] == "..":
                        path_node = os.path.dirname(path_node)  # Назначение нового пути (родительской директории)
                        os.chdir(path_node)  # Изменение текущей директории
                    elif os.path.isdir(path_node + os.sep + lis[1]):  # Проверка на существование директории
                        os.chdir(path_node + os.sep + lis[1])
                        path_node = path_node + os.sep + lis[1]
                    else:
                        print("Такой директории не найдено!", path_node + os.sep + lis[1])
                    if len(path_node) >= len(save_node):
                        print("Current dir:", path_node)


                elif lis[0] == "mkfile":
                    for i in range(1, len(lis)):  # Создаем один или несколько файлов по назначенным через пробел именам 
                        print("Создаем файл "+lis[i])
                        mkfile(path_node + os.sep + lis[i])
                elif lis[0] == "wrfile":
                    wrfile(path_node + os.sep + lis[1])
                elif lis[0] == "catfile":
                    catfile(path_node + os.sep + lis[1])
                elif lis[0] == "rmf":
                    for i in range(1, len(lis)):
                        rmf(lis[i])  # Удаляем один или несколько файлов по назначенным именам через пробел
                elif lis[0] == "cpfile":
                    if lis[2] == '..':
                        path_node_tmp = os.path.dirname(path_node)  # Временная переменная для определения родительской директории
                        if len(path_node_tmp) < len(save_node):
                            print("Вы находитесь в корневой директории!")
                        else:
                            cpfile(path_node + os.sep + lis[1], path_node_tmp)
                    else:
                        cpfile(path_node + os.sep + lis[1], path_node + os.sep + lis[2])
                elif lis[0] == "mvfile":
                    if lis[2] == '..':
                        path_node_tmp = os.path.dirname(path_node)
                        if len(path_node_tmp) < len(save_node):
                            print("Вы находитесь в корневой директории!")
                        else:
                            mvfile(path_node + os.sep + lis[1], path_node_tmp)
                    else:
                        mvfile(path_node + os.sep + lis[1], path_node + os.sep + lis[2])
                elif lis[0] == "renamef":
                    renamef(path_node + os.sep + lis[1], path_node + os.sep + lis[2])
            else:
                print("Проверьте наличие синтаксической ошибки в команде и корректность аргументов!")
            command = input("Введите команду: ")
        else:
            print("Вы не можете покинуть корневую директорию, вы были возвращены к корневой папке")
            print("Current dir:", save_node)
            path_node = save_node
            continue


main()