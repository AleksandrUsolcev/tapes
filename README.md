# tapes

Микроблог/соцсетка, песочница созданная в учебных целях которая будет периодически обрастать "мясом" из новых функций. В текущем виде прикручен редактор профиля, можно создавать тематические ленты, добавлять в закладки/лайкать/каментить посты, фолловить авторов.

В текущем состоянии адаптивность верстки отсутствует, некоторые элементы фронта могут иметь проблемы, рекомендуемое разрешение >= 1920х1080, что так же будет исправлено.

### Используемые расширения

- [django-htmx](https://github.com/adamchainz/django-htmx)
- [django-client-side-image-cropping](https://github.com/koendewit/django-client-side-image-cropping)
- [django-quill-editor](https://github.com/LeeHanYeong/django-quill-editor)
- [django-bootstrap-modal-forms](https://github.com/trco/django-bootstrap-modal-forms)

### Запуск проекта

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
python3 manage.py migrate
python3 manage.py runserver
``` 
