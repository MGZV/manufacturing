<h1 align="center">Производство</h1>

---
Это приложение позволяет расчитать материальные и трудовые затраты 
необходимые для выполнения производственного плана.

На данном этапе заполнение данных выполняется в админке.

План производства можно сформировать добавляя:
- изделия;
- сборочные узлы;
- детали;
- другие работы.

Калькулятор посчитает исходя из производственного плана
необходимое количество:
- материала;
- стандартных изделий;
- норм часов на операции.
---

# Установка

Необходимо склонировать приложение. Создать виртуальное окружение.
Переименовать **.env-sample** в **.env**
Выполнить:
```Python
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python createsuperuser # создать суперюзера
python manage.py runserver
```
Дальнейшая работа выполняется в админке.
Есть импортировать: материалы, операции, стандартные изделия из документа
Excel. 

Для этого нужно: 
- раскомментировать STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
- закоментировать STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
```Python
python manage.py collectstatic
```
- закоментировать STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
- раскомментировать STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

