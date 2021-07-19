# shop_api
API for online_shop

### Зависимости для сборки
- requirements.txt

### Инструкция по сборке (linux)
`sudo apt update`  
`sudo apt install postgresql postgresql-contrib`  
`sudo -u postgres psql`  
`CREATE USER shop WITH PASSWORD 'shop';`  
`CREATE DATABASE shop_api OWNER shop;`   
`ALTER ROLE shop WITH LOGIN;`   
`GRANT ALL PRIVILEGES ON DATABASE shop_api TO shop;`

`sudo apt install python3`  
`python3 -m venv env`   
`source env/bin/activate`   
`pip install -r requirements.txt`   
`cd shop`   
`python manage.py migrate`  
`python manage.py createsuperuser`  
- придумать логин и пароль
- далее используется базовая авторизация для api-запросов   

`python manage.py runserver 0.0.0.0:8000`   

## Работа с API
### Создание товара
url:

`http://0.0.0.0:8000/api/product/`

метод POST
формат json:

```json
{
    "sku": "fff1234567890123456",
    "cost": 100,
    "type": [
        {
            "typeUid": 1,
            "typeName": "computer"
        }
    ],
    "name": "iMac"
}
```

возможно множество категорий

```json
{
    "sku": "fff1234567890123456",
    "cost": 100,
    "type": [
        {
            "typeUid": 1,
            "typeName": "computer"
        },
        {
            "typeUid": 2,
            "typeName": "mono"
        }
    ],
    "name": "iMac"
}
```

возвращает UID

### Получение каталога товаров

- Получить все товары

url:

`http://0.0.0.0:8000/api/products/`

метод GET

возвращает все товары

- Получить диапазон товаров

url:

`http://0.0.0.0:8000/api/products/<begin>-<end>`

метод GET

где `<begin>` — целочисленное значение начала запрашиваемого диапазона

где `<end>` — целочисленное значение конца запрашиваемого диапазона

возвращает запрашиваемый диапазон товаров, если существует

- Получить определенный товар по UID

url:

`http://0.0.0.0:8000/api/product/uid/<uid>`

метод GET

где `<uid>` — uid товара

возвращает запращиваемый товар, если uid существует

- Получить определенный товар по SKU

url:

`http://0.0.0.0:8000/api/product/sku/<sku>`

метод GET

где `<sku>` — sku товара

возвращает запращиваемый товар, если sku существует

### Удаление товаров

- Удалить определенный товар по UID

url:

`http://0.0.0.0:8000/api/product/delete/uid/<uid>`

метод DELETE

где `<uid>` — uid товара

Удаляет товар, если uid существует

- Удалить определенный товар по SKU

url:

`http://0.0.0.0:8000/api/product/delete/sku/<sku>`

метод DELETE

где `<sku>` — sku товара

Удаляет товар, если sku существует

### Обновление товаров

- Обновить определенный товар по UID

url:

`http://0.0.0.0:8000/api/product/update/uid/<uid>`

метод PATCH

где `<uid>` — uid товара

форматы json:

```json
{
    "type": [
        {
            "typeUid": 10,
            "typeName": "computers10"
        },
        {
            "typeUid": 12,
            "typeName": "aa"
        }
    ],
    "sku": "fff1234567890123777810",
    "name": "appleggg",
    "cost": "77710.00"
}
```

```json
{
    "type": [
        {
            "typeUid": 10,
            "typeName": "computers10"
        }
    ],
    "sku": "fff1234567890123777810",
    "name": "appleggg",
    "cost": "77710.00"
}
```

```json
{
    "sku": "fff1234567890123777810",
    "name": "appleggg",
    "cost": "77710.00"
}
```

```json
{
    "name": "appleggg",
    "cost": "77710.00"
}
```

и другие...

Обновляет товар, если uid существует

- Обновить определенный товар по SKU

url:

`http://0.0.0.0:8000/api/product/update/sku/<sku>`

метод PATCH

где `<sku>` — sku товара

форматы json:

```json
{
    "type": [
        {
            "typeUid": 10,
            "typeName": "computers10"
        },
        {
            "typeUid": 12,
            "typeName": "aa"
        }
    ],
    "sku": "fff1234567890123777810",
    "name": "appleggg",
    "cost": "77710.00"
}
```

```json
{
    "type": [
        {
            "typeUid": 10,
            "typeName": "computers10"
        }
    ],
    "sku": "fff1234567890123777810",
    "name": "appleggg",
    "cost": "77710.00"
}
```

```json
{
    "sku": "fff1234567890123777810",
    "name": "appleggg",
    "cost": "77710.00"
}
```

```json
{
    "name": "appleggg",
    "uid": "857d2b80-d0b1-4bc5-9cfd-b5865f179cec"
}
```

и другие...

Обновляет товар, если sku существует