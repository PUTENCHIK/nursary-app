# Приложение питомника для собак nursary-app

## Структура базы данных

`users(id, login, password, is_deleted)`\
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
        "message": "Exception description",
        "code": 801
    }

}
```

## users_router

### Вход в учётную запись
`/users/signin`

* Request
```
{
    login: "user123",
    password: "superuser"
}
```
* Response
```
{
    success: true,
    exception: null
}
```
