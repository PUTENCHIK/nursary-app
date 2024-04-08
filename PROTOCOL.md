# Протокол приложения nursary-app

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
* Ответ
```
{
    id: 100,
    login: "user123",
    token: "abc123",
    is_admin: false
}
```

### Регистрация новой учётной записи
Если is_admin = true, то проверяется переданный токен с хешированным токеном приложения. Если токены совпадают, в БД новая учётная запись отмечается как админская.

Если is_admin = false, то значение переданного токена не используется.

`/users/signup`

* Запрос
```
{
    login: "user123",
    password: "superuser",
    is_admin: true,
    admin_token: "admin_token"
}
```
* Ответ
```
{
    id: 100,
    login: "user123",
    token: "abc123",
    is_admin: false
}
```

### Удаление учётной записи
`/users/remove`

* Запрос
```
{
    login: "user123",
    password: "superuser"
}
```
{
    success: true
}

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
* Ответ
```
{
    id: 101,
    login: "123user",
    token: "def456",
    is_admin: false
}
```




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
Функция доступна только пользователям-админам.

`/tasks/add_template`

* Запрос
```
{
    text: "Всем привет, и сегодня вам нужно покормить 100 собак.",
    login: "admin_login",
    password: "admin_password"
}
```
* Базовый ответ

### Добавление нового задания пользователем
`/tasks/add_task`

* Запрос
```
{
    collar_id: 321,
    template_id: 101,
    login: "user123",
    password: "superuser"
}
```
* Базовый ответ
