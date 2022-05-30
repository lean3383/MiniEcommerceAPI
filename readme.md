# MiniEcommerce

Prueba de conocimiento para ClickOh

## Despliegue

El servicio se encuenta desplagado en la siguiente url

```html
  https://yy2bj2urpx.us-east-1.awsapprunner.com/
```
Para obtener token utilizar la siguente cuenta
```html
  USER= app
  PASS= pass2022
```

## Para ejecutar localmente

Descargar el proyecto

```bash
  git clone https://github.com/lean3383/MiniEcommerceAPI.git
```

Ingresar el directorio del proyecto y realizar el build

```bash
  docker-compose build
```

Iniciar el servicio

```bash
  docker-compose up
```

## Variables de entorno
Para ejecutar el proyecto, es necesario agregar las siguientes variables en un archivo .env

`SECRET_KEY`
`DEBUG`
`HOST`

## Ejecutar Tests

Ejecutar las pruebas, con el siguiente comando
```bash
  docker-compose run backend python manage.py test
```

## Referencia API

### Obtener token de acceso

```html
  POST api/token/
```
#### Parametros JSON

| Parametro  | Tipo                   |
|  --------- |  --------------------- |
| `username` | 'string' **Requerido** |
| `password` | 'string' **Requerido** |

#### Ejemplo

Request
```json
{
  "username": "app",
  "password": "pass2022"
}
```
Response
```json
{
"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1Mzk0Njg4MiwiaWF0IjoxNjUzODYwNDgyLCJqdGkiOiI1NTZhNGYwMTlkYzQ0MmRjODQxZGI0NWExYjJkNzU0MSIsInVzZXJfaWQiOjF9.6ZPmnv7ALUFiSz2PyeoGV2yq7OGhX0Jp17ktxEgaGiM",
"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzODYwNzgyLCJpYXQiOjE2NTM4NjA0ODIsImp0aSI6IjdkYmU5YzlhYmUxNjRhM2ViYjc1ZDczODQyMWIzNDUwIiwidXNlcl9pZCI6MX0.TY35dmsB0vjx0eo7RKslonf-AmW6ErUzCYAEZ1jZUxA"
}
```

### Obtener todos los productos

```html
  GET product/
  * Es requerido incluir token de acceso en header
```

#### Ejemplo

Response
```json
[
  {
    "id": "PK2",
    "name": "Leche",
    "price": 100,
    "stock": 1
  },
  {
    "id": "PK3",
    "name": "Arroz",
    "price": 100,
    "stock": 1
  }
]
```

### Obtener un producto en particular

```html
  GET product/<id de producto>/
  * Es requerido incluir token de acceso en header
```

#### Ejemplo

Response
```json
{
  "id": "PK2",
  "name": "Leche",
  "price": 100,
  "stock": 1
}
```

### Crear un producto nuevo

```html
  POST product/
  * Es requerido incluir token de acceso en header
```

#### Parametros JSON

| Parametro | Tipo                   | Notas |
|  -------- |  --------------------- | ----- |
| `id`      | 'string' | **Requerido.**
| `name`    | 'string' | **Requerido.**
| `price`   | 'float'  | **Requerido.** Debe ser mayor a 0
| `stock`   | 'int     | **Opcional.** No debe ser negativo. Si no se incluye, se ingresa con 0 unidades

#### Ejemplo

Request
```json
{
  "id": "PK2",
  "name": "Leche",
  "price": 100
}
```
Response
```json
{
  "id": "PK2",
  "name": "Leche",
  "price": 100,
  "stock": 0
}
```

### Eliminar un producto

```html
  DELETE product/<id de producto>/
  * Es requerido incluir token de acceso en header
```

### Modificar un producto

```html
  POST product/<id de producto>/
  * Es requerido incluir token de acceso en header
```

#### Parametros JSON

| Parametro | Tipo     | Notas |
|  -------- |  ------- | ----- |
| `name`    | 'string' | **Opcional.**
| `price`   | 'float'  | **Opcional.** Debe ser mayor a 0
| `stock`   | 'int'    | **Opcional.** No debe ser negativo. Si no se incluye, se ingresa con 0 unidades

#### Ejemplo

Request (modifica solo stock)
```json
{
  "stock": 10
}
```
Response
```json
{
  "id": "PK2",
  "name": "Leche",
  "price": 100.5,
  "stock": 10
}
```

### Obtener todas las ordenes

```html
  GET order/
  * Es requerido incluir token de acceso en header
```

#### Ejemplo

Response
```json
[
  {
    "id": "FAC1",
    "order_details": [
      {
        "quantity": 3,
        "product": "PK2"
      }
    ],
    "total": 2000,
    "total_usd": 9.61,
    "date_time": "2022-05-26T21:37:33.992783Z"
  },
  {
    "id": "FAC2",
    "order_details": [
      {
        "quantity": 3,
        "product": "PK1"
      }
    ],
    "total": 75,
    "total_usd": 0.36,
    "date_time": "2022-05-26T21:43:57.771653Z"
  }
]
```

### Obtener una orden en particular

```html
  GET order/<id de order>/
  * Es requerido incluir token de acceso en header
```

#### Ejemplo

Response
```json
{
  "id": "FAC2",
  "order_details": [
    {
      "quantity": 3,
      "product": "PK1"
    }
  ],
  "total": 75,
  "total_usd": 0.36,
  "date_time": "2022-05-26T21:43:57.771653Z"
}
```
### Crear una orden

```html
  POST order/
  * Es requerido incluir token de acceso en header
```

#### Parametros JSON

| Parametro       | Tipo     | Notas |
|  -------------- |  ------- | ----- |
| `id`            | 'string' | **Requerido.**
| `order_details` | 'list'   | **Requerido.**
|  - `product`    | 'string' | **Requerido.** El id del producto deseado
|  - `quantity`   | 'int'    | **Requerido.** Debe ser mayor a 0


#### Ejemplo

Request
```json
{
  "id": "FAC100",
  "order_details": [
    {
      "quantity": 1,
      "product": "PK2"
    }
  ]
}
```
Response
```json
{
  "id": "FAC100",
  "order_details": [
    {
      "quantity": 1,
      "product": "PK2"
    }
  ],
  "total": 75,
  "total_usd": 0.36,
  "date_time": "2022-05-29T23:06:18.414996Z"
}
```

### Eliminar una orden

```html
  DELETE order/<id de order>/
  * Es requerido incluir token de acceso en header
```

### Modificar una orden

```html
  POST order/<id de order>/
  * Es requerido incluir token de acceso en header
```

#### Parametros JSON

| Parametro       | Tipo     | Notas |
| --------------  | -------  | ----- |
| `order_details` | 'list'   | **Requerido.** |
|    - `product`  | 'string' | **Requerido.**. El id del producto deseado |
|    - `quantity`   | 'int'    | **Requerido.** Debe ser mayor a 0 |


#### Ejemplo

Request
```json
{
  "order_details": [
    {
      "quantity": 2,
      "product": "PK2"
    }
  ]
}
```
Response
```json
{
  "id": "FAC100",
  "order_details": [
    {
      "quantity": 2,
      "product": "PK2"
    }
  ],
  "total": 75,
  "total_usd": 0.36,
  "date_time": "2022-05-29T23:06:18.414996Z"
}
```

## Notas Finales

 - El sistema se encarga de mantener la integridad del numero de stock de acuerdo a los pedidos y sus modificaciones
 - Se utiliza el framework de cache para no realizar requests inncesarios, este valor se actualiza cada 5 minutos de ser necesario
