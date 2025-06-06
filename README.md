# Документация DH|Platform

## Описание

Данный пакет предназначен для базовых механизмов продуктов DH

## Установка

```commandline
poetry add git+https://github.com/JohnSoi/dh-platform.git
```

Если планируется активное разработка в пакете, то лучше добавить локальную зависимость:
```commandline
poetry add ../dh-platform --group dev
```


## Состав

<pre>
dh_platform
├── models
│   ├── mixins
│   └── models
├── schemas
│   └── mixins
└── settings
</pre>

## Полезные команды

### Автодокументация
Документация будет находиться в каталоге: ```docs/_build/index.html```

* Инициализация документации:
```commandline
mkdir docs
cd docs
sphinx-quickstart
```
Далее нужно ответить на несколько вопросов

* Для создания автодокументации нужно перейти в каталог ```docs```:
```commandline
cd docs
```

#### Cоздание документации

```commandline
make html 
```

#### Проверка покрытия документацией

```commandline
make coverage 
```