# tapes
![Python version](https://img.shields.io/badge/python-3.7-yellow) ![Django version](https://img.shields.io/badge/django-3.2-orange)

Микроблог/соцсетка написанная в учебных целях которая будет периодически обрастать "мясом" из новых функций. В текущем виде прикручен редактор профиля, можно создавать тематические ленты, добавлять в закладки/лайкать/комментировать посты, фолловить авторов.

Пока что адаптивность верстки отсутствует, некоторые элементы фронта могут иметь проблемы, рекомендуемое разрешение >= 1920х1080, что так же будет исправлено.

## Сторонние расширения Django

- [django-htmx](https://github.com/adamchainz/django-htmx)
- [django-client-side-image-cropping](https://github.com/koendewit/django-client-side-image-cropping)
- [django-quill-editor](https://github.com/LeeHanYeong/django-quill-editor)
- [django-bootstrap-modal-forms](https://github.com/trco/django-bootstrap-modal-forms)

## Запуск проекта

Клонировать репозиторий, установить и активировать виртуальное окружение

```
# mac/linux
python3 -m venv venv
source venv/bin/activate 
# win
py -m venv venv
source venv/Scripts/activate 
``` 

Установить зависимости из файла requirements.txt

```
pip install -r requirements.txt
``` 

Выполнить миграции и запустить проект

```
cd tapes
py manage.py migrate
py manage.py runserver
``` 
