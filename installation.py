import os
print("Настройки файлового менеджера \n")
print("Текущая рабочая папка/директория: ", os.getcwd())
workdir = input("Установка корневой директории (введите полный путь): ")
def get_wd(workdir):
    try:
        os.chdir(workdir)
    except FileNotFoundError:
        print("Вы создали новую директорию.")
        os.mkdir(workdir)
        os.chdir(workdir)

get_wd(workdir)
print("Текущая рабочая папка: ", os.getcwd())