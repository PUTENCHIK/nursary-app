# Приложение питомника для собак nursary-app

## Структура базы данных

`users(id, login, password, is_admin, is_deleted)` &emsp;// поле is_admin отражает то, есть ли у учётной записи дополнительные функции: работа с ошейниками и собаками\
`collars(id, code)` &emsp;// таблица ошейники (только технические характеристики)\
`exploits(id, collar_id, dog_id, start_exploit, end_exploit)` &emsp;// записи об отслеживаемых ошейниках, собаках с этими ошейниками и времеными рамками эксплуатации ошейников\
`dogs(id, name, location)`\
`task_templates(id, text, id_deleted)` &emsp;// предопределённые задания для пользователей (может редактировать только админ)\
`tasks(id, author_id, collar_id, template_id, is_done, is_deleted)` &emsp;// создаваемые пользователями задания, связанные с определёнными отслеживаемыми собаками. is_done устанавливает автор задания\
`responses(id, author_id, task_id, image_path, is_deleted)`  &emsp;// таблица откликов пользователей на конкретные задания с указанием пути на фотоотчёт

## Базовые формы запросов и ответов

* Успешный запрос 
```
{
    success: true,
    exception: null
}
```
* Проваленый запрос
```
{
    success: false,
    exception: {
        message: "Exception description",
        code: 801
    }
}
```

## users_router

### Вход в учётную запись
`/users/signin`

* Запрос
```
{
    login: "user123",
    password: "superuser"
}
```
* Базовый ответ

### Регистрация новой учётной записи
Если is_admin = true, то проверяется переданный токен с хешированным токеном приложения. Если токены совпадают, в БД новая учётная запись отмечается как админская.\
Если is_admin = false, то значение переданного токена не используется.\
`/users/signup`

* Запрос
```
{
    login: "user123",
    password: "superuser",
    is_admin: true,
    token: "special_token"
}
```
* Базовый ответ

### Удаление учётной записи
`/users/remove`

* Запрос
```
{
    login: "user123",
    password: "superuser"
}
```
* Базовый ответ

### Изменение логина и/или пароля учётной записи
`/users/change`

* Запрос
```
{
    login: "user123",
    password: "superuser",
    new_login: "123user",
    new_password: "password"
}
```
* Базовый ответ

## collars_router
Все функции из этого роутера доступны только пользователям-админам.

### Добавление в БД новой собаки
`/collars/add_dog`

* Запрос
```
{
    name: "Ralfy",
    location: "Irkutsk",
    login: "admin_login",
    password: "admin_password"
}
```
* Базовый ответ

### Добавление в БД нового ошейника
`/collars/add_collar`

* Запрос
```
{
    code: "123abc456",
    login: "admin_login",
    password: "admin_password"
}
```
* Базовый ответ

### Привязка ошейника к определённой собаке
`/collars/link`

* Запрос
```
{
    collar_id: 123,
    dog_id: 456,
    login: "admin_login",
    password: "admin_password"
}
```
* Базовый ответ

### Удаление собаки из БД
`/collars/remove_dog`

* Запрос
```
{
    dog_id: 123,
    login: "admin_login",
    password: "admin_password"
}
```
* Базовый ответ

### Удаление ошейника из БД
`/collars/remove_collar`

* Запрос
```
{
    collar_id: 123,
    login: "admin_login",
    password: "admin_password"
}
```
* Базовый ответ

### Отвязка ошейника от определённой собаке
`/collars/unlink`

* Запрос
```
{
    collar_id: 123,
    dog_id: 456,
    login: "admin_login",
    password: "admin_password"
}
```
* Базовый ответ

## tasks_router

### Добавление нового шаблона заданий
Функция доступна только пользователям-админам.\
`/tasks/add_template`


