# my_job_helpers

# Программы помощники для скачивания и обработки отчетов

## Описание

### Проект содержит три программы - DownLoader, Temperature, 70_otchet

### DownLoader - загрузчик и обработчик отчетов по работе на оптовом рынке электроэнергии и мощности с сайта Коммерческого оператора АО "АТС". В файле 0_коды_АТС.txt построчно указываются компании и параметры доступа на сайт в следующем формате: company_name login code password. При запуске программы разворачиваетс GUI интерфейс, в котором можно выбрать нужные компании, отчеты, периоды. Скачивание организовано через пакет selenium посредством кликов по соответствующим ссылкам на сайте. Отчеты сохраняются на в папку

### Автор уже может выбрать имя и уникальный адрес для своей страницы. Дизайн пока что самый простой.

### Возможно нужно будет реализовать возможность модерировать записи и блокировать пользователей, если начнут присылать спам.

### Записи можно отправить в сообщество и посмотреть там записи разных авторов.

## Как установить проект

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AKafer/SOSBLOG.git
cd SOSBLOG/
```

### Создать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
cd yatube
python manage.py migrate
```

### Запустить проект:

```
python manage.py runserver
```

## Стек технологий

### Python 3, Django 2.2, PostgreSQL, gunicorn, nginx, Яндекс.Облако(Ubuntu 18.04), pytest

## Автор проекта - Сергей Сторожук

