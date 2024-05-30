# Протокол приложения nursary-app

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
* Ответ
```
{
    success: true
}
```

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
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    dog_id: 123
}
```

### Добавление в БД нового ошейника
`/collars/add_collar`

* Запрос
```
{
    code: "123abc456",
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    collar_id: 123
}
```

### Привязка ошейника к определённой собаке
`/collars/link`

* Запрос
```
{
    collar_id: 123,
    dog_id: 456,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    success: true
}
```

### Удаление собаки из БД
`/collars/remove_dog`

* Запрос
```
{
    dog_id: 456,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    success: true
}
```

### Удаление ошейника из БД
`/collars/remove_collar`

* Запрос
```
{
    collar_id: 456,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    success: true
}
```

### Отвязка ошейника от определённой собаке
`/collars/unlink`

* Запрос
```
{
    collar_id: 123,
    dog_id: 456,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    success: true
}
```





## tasks_router

### Добавление нового задания пользователем
`/tasks/add_task`

* Запрос
```
{
    collar_id: 321,
    text: "Всем привет, и сегодня вам нужно будет собаку!",
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    task_id: 201
}
```

### Размещение отклика на задание
`/tasks/add_response`

* Запрос
```
{
    task_id: 321,
    image_path: https://host/images/answer.png,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    response_id: 201
}
```

### Подтверждение автором задания отклика на это задание
`/tasks/confirm_response`

* Запрос
```
{
    response_id: 321,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    success: true
}
```

### Удаление задания
Пользователь может удалять задания, на которые ещё нет ни одного ответа
`/tasks/remove_task`

* Запрос
```
{
    task_id: 321,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    success: true
}
```

### Удаление отклика
`/tasks/remove_response`

* Запрос
```
{
    response_id: 321,
    user_token: "QWE123RTY"
}
```
* Ответ
```
{
    success: true
}
```

### Получение заданий автора
`/tasks/get_tasks`

* Запрос
```
{
    author_id: 1,
}
```
* Ответ
```
{
    [
        {
            id: 2,
            collar_id: 102,
            text: "Помогите собаке!"
        },

        {
            id: 4,
            collar_id: 104,
            text: "Покормите собаку!"
        }
    ]
}
```
