import os
from installation import *
import shutil
print("Список команд для ввода:"
      "\n1 - crdir [dir name] - Создание папки с указанием имени"
      "\n2 - deldir [dir name] - Удаление папки по имени"
      "\n3 - cddir [dir name] - cddir .. - Перемещение между папками - заход в папку по имени, выход на уровень вверх"
      "\n4 - mkfile [filename1 filename2 ...] - Создание пустых файлов с указанием имени"
      "\n5 - wrfile [filename]- Запись текста в файл"
      "\n6 - catfile [filename]- Просмотр содержимого текстового файла"
      "\n7 - rmf [filename1 filename2 ...] - Удаление файлов по имени"
      "\n8 - cpfile [filename folder] - Копирование файлов из одной папки в другую"
      "\n9 - mvfile [filename folder] - Перемещение файлов"
      "\n10 - renamef [filename] [new_filename] - Переименование файлов")

command = input("Введите команду: ")
all_commands = ["crdir", "deldir", "cddir", "mkfile", "wrfile", "catfile", "rmf", "cpfile", "mvfile", "renamef"]
node = os.path.abspath(wd)
save_node = node
path_node = node+"/"
def crdir(dirname):
    global node
    print("Создание папки "+dirname)
    os.mkdir(node+"/"+dirname)


def deldir(dirname):
    global node
    print("Удаление папки "+dirname)
    os.rmdir(node+"/"+dirname)


def cddir(dirname):
    global node
    print("Перемещение в каталог "+dirname)
    os.chdir(path_node+dirname)


def mkfile(filename):
    open(filename, "w")


def wrfile(filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(input())


def catfile(filename):
    with open(path_node+filename, 'r') as f:
        data = f.read()
        print(data)


def rmf(filename):
    print("Удаление файла...")
    os.remove(filename)


def cpfile(filename, path):
    print("Копирование файла...")
    shutil.copy(filename, path, follow_symlinks=True)


def mvfile(filename, path):
    print("Перемещение файла...")
    if os.path.isfile(filename):
        shutil.move(filename, path)


def renamef(filename, new_filename):
    print("Переименование файла...")
    if os.path.isfile(filename):
        shutil.move(filename, new_filename)


while command != 'exit':
    if save_node in node:
        lis = command.split()
        if lis[0] in all_commands and len(lis) > 1:
            if lis[0] == "crdir":
                try:
                    crdir(lis[1])
                except FileExistsError:
                    print('Директория с таким названием уже существует!')
            elif lis[0] == "deldir":
                if os.path.isdir(path_node+lis[1]):
                    try:
                        deldir(lis[1])
                    except OSError:
                        ok = input("Папка не пуста, вы уверены, что хотите удалить её? Нажмите Y")
                        if ok == "Y":
                            shutil.rmtree(path_node+lis[1])
                        else:
                            pass
            elif lis[0] == "cddir":
                print("Current dir:", os.getcwd())
                if os.path.isdir(os.getcwd()+"\\"+lis[1]):
                    os.chdir(path_node+lis[1])
                elif lis[1] == "..":
                    os.chdir(os.path.basename(node))
                else:
                    print("Такой директории не найдено!")
                print("Current dir:", os.getcwd())
                node = os.getcwd()
            elif lis[0] == "mkfile":
                for i in range(1, len(lis)):
                    print("Создаем файл "+lis[i])
                    mkfile(path_node+lis[i])
            elif lis[0] == "wrfile":
                wrfile(path_node+lis[1])
            elif lis[0] == "catfile":
                catfile(path_node+lis[1])
            elif lis[0] == "rmf":
                for i in range(1, len(lis)):
                    rmf(lis[i])
            elif lis[0] == "cpfile":
                cpfile(path_node+lis[1], path_node+lis[2])
            elif lis[0] == "mvfile":
                mvfile(path_node+lis[1], path_node+lis[2])
            elif lis[0] == "renamef":
                renamef(path_node+lis[1], path_node+lis[2])
        else:
            print("Проверьте наличие синтаксической ошибки в команде и корректность аргументов!")
        command = input("Введите команду: ")
    else:
        print("Вы не можете покинуть корневую директорию, вы были возвращены к корневой папке")
        node = save_node
        continue