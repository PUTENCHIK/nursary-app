# Структура базы данных приложения

## Таблицы

### users

```sql
users(
    id INT unsigned not null auto_increment primary key,        -- уникальное id пользователя
    login VARCHAR(255) not null unique,                         -- уникальный логин пользователя в нижнем регистре
    password VARCHAR(255) not null,                             -- хешированный пароль пользователя
    token VARCHAR(255) not null unique,                         -- уникальный токен пользвателя, использующийся для подтверждения действий в приложении
    is_admin BOOLEAN not null default 0,                        -- если true, то пользователю доступны все функции приложения, если же false, то только авторизация и функции, связанные с заданиями
    is_deleted BOOLEAN not null default 0                       -- мягкое удаление записи из БД
)
```

### collars

```sql
collars(
    id INT unsigned not null auto_increment primary key,        -- уникальное id ошейника
    code VARCHAR(255)                                           -- заводской код ошейника
    is_deleted BOOLEAN not null default 0                       -- мягкое удаление записи из БД
)
```

### exploits

```sql
exploits(
    id INT unsigned not null auto_increment primary key,        -- уникальное id записи эксплуатации
    collar_id INT unsigned not null,                            -- id ошейника, который "отдали" определённой собаке
    dog_id INT unsigned not null,                               -- id собаки, которой "отдали" ошейник на время эксплуатации
    start_exploit DATETIME not null,                            -- дата и время начала эксплуатации ошейника (по умолчанию - время добавление записи в БД)
    end_exploit DATETIME default null                           -- дата и время конца эксплуатации ошейника (по умолчанию - null, меняется на дату и время при "передаче" ошейника другой собаке)
)
```

### dogs

```sql
dogs(
    id INT unsigned not null auto_increment primary key,        -- уникальное id собаки
    name VARCHAR(255) not null,                                 -- кличка собаки
    location VARCHAR(255) not null default "Unknown",           -- уточнение об известном месте обитания собаки
    is_deleted BOOLEAN not null default 0                       -- мягкое удаление записи из БД
)
```

### tasks

```sql
tasks(
    id INT unsigned not null auto_increment primary key,        -- уникальное id задания
    author_id INT unsigned not null,                            -- id автора задания
    collar_id INT unsigned not null,                            -- id ошейника собаки, к которой относится задание
    text MEDIUMTEXT not null,                                   -- текстовое описание шаблона задания
    created_at DATETIME not null,                               -- дата и время добавления задания
    is_deleted BOOLEAN not null default 0                       -- мягкое удаление записи из БД
)
```

### responses

```sql
responses(
    id INT unsigned not null auto_increment primary key,        -- уникальное id отклика
    author_id INT unsigned not null,                            -- id пользователя, оставившего отклик
    task_id INT unsigned not null,                              -- id задания 
    image_path VARCHAR(255) not null,                           -- путь к изображению, загруженного пользователем как подтвеждение ответа
    created_at DATETIME not null,                               -- дата и время добавления отклика
    is_confirmed BOOLEAN not null default 0                     -- является ли отклик подтверждённым автором задания (одновременно может быть подтверждён только один отклик к каждому заданию)
    confirmed_at DATETIME not null,                             -- дата и время подтверждения отклика
    is_deleted BOOLEAN not null default 0                       -- мягкое удаление записи из БД
)
```

