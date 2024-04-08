# Структура базы данных приложения

## Таблицы

### users

```
users(
  id INT unsigned not null auto_increment primary key, &emsp;&emsp;&emsp;//
  login VARCHAR(255) not null unique,&emsp;&emsp;&emsp;//
  password VARCHAR(255) not null,&emsp;&emsp;&emsp;//
  token VARCHAR(255) not null unique,&emsp;&emsp;&emsp;//
  is_admin BOOLEAN not null default 0,&emsp;&emsp;&emsp;//
  is_deleted BOOLEAN not null default&emsp;&emsp;&emsp;//
)
```
&emsp;// поле is_admin отражает то, есть ли у учётной записи дополнительные функции: работа с ошейниками и собакам

### collars

`collars(id, code)` &emsp;// таблица ошейники (только технические характеристики)

### exploits

`exploits(id, collar_id, dog_id, start_exploit, end_exploit)` &emsp;// записи об отслеживаемых ошейниках, собаках с этими ошейниками и времеными рамками эксплуатации ошейников

### dogs

`dogs(id, name, location)`

### task_templates

`task_templates(id, text, id_deleted)` &emsp;// предопределённые задания для пользователей (может редактировать только админ)

### tasks

`tasks(id, author_id, collar_id, template_id, is_done, is_deleted)` &emsp;// создаваемые пользователями задания, связанные с определёнными отслеживаемыми собаками. is_done устанавливает автор задания

### responses

`responses(id, author_id, task_id, image_path, is_deleted)`  &emsp;// таблица откликов пользователей на конкретные задания с указанием пути на фотоотчёт

## Описание таблиц и их полей