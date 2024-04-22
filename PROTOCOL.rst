
Протокол приложения nursary-app
===============================

Базовые формы запросов и ответов
--------------------------------


* Успешный запрос 
  .. code-block::

     {
       success: true,
       exception: null
     }

* Проваленый запрос
  .. code-block::

     {
       success: false,
       exception: {
           message: "Exception description",
           code: 801
       }
     }

users_router
------------

Вход в учётную запись
^^^^^^^^^^^^^^^^^^^^^

``/users/signin``


* Запрос
  .. code-block::

     {
       login: "user123",
       password: "superuser"
     }

* Ответ
  .. code-block::

     {
       id: 100,
       login: "user123",
       token: "abc123",
       is_admin: false
     }

Регистрация новой учётной записи
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Если is_admin = true, то проверяется переданный токен с хешированным токеном приложения. Если токены совпадают, в БД новая учётная запись отмечается как админская.

Если is_admin = false, то значение переданного токена не используется.

``/users/signup``


* Запрос
  .. code-block::

     {
       login: "user123",
       password: "superuser",
       is_admin: true,
       admin_token: "admin_token"
     }

* Ответ
  .. code-block::

     {
       id: 100,
       login: "user123",
       token: "abc123",
       is_admin: false
     }

Удаление учётной записи
^^^^^^^^^^^^^^^^^^^^^^^

``/users/remove``


* Запрос
  .. code-block::

     {
       login: "user123",
       password: "superuser"
     }

* Ответ
  .. code-block::

     {
       success: true
     }

Изменение логина и/или пароля учётной записи
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/users/change``


* Запрос
  .. code-block::

     {
       login: "user123",
       password: "superuser",
       new_login: "123user",
       new_password: "password"
     }

* Ответ
  .. code-block::

     {
       id: 101,
       login: "123user",
       token: "def456",
       is_admin: false
     }

collars_router
--------------

Все функции из этого роутера доступны только пользователям-админам.

Добавление в БД новой собаки
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/collars/add_dog``


* Запрос
  .. code-block::

     {
       name: "Ralfy",
       location: "Irkutsk",
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       dog_id: 123
     }

Добавление в БД нового ошейника
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/collars/add_collar``


* Запрос
  .. code-block::

     {
       code: "123abc456",
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       collar_id: 123
     }

Привязка ошейника к определённой собаке
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/collars/link``


* Запрос
  .. code-block::

     {
       collar_id: 123,
       dog_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       collar_id: 123,
       dog_id: 456
     }

Удаление собаки из БД
^^^^^^^^^^^^^^^^^^^^^

``/collars/remove_dog``


* Запрос
  .. code-block::

     {
       dog_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       dog_id: 456
     }

Удаление ошейника из БД
^^^^^^^^^^^^^^^^^^^^^^^

``/collars/remove_collar``


* Запрос
  .. code-block::

     {
       collar_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       collar_id: 456
     }

Отвязка ошейника от определённой собаке
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/collars/unlink``


* Запрос
  .. code-block::

     {
       collar_id: 123,
       dog_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       collar_id: 123,
       dog_id: 456
     }

tasks_router
------------

Добавление нового шаблона заданий
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Функция доступна только пользователям-админам.

``/tasks/add_template``


* Запрос
  .. code-block::

     {
       text: "Всем привет, и сегодня вам нужно покормить 100 собак.",
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       template_id: 102
     }

Добавление нового задания пользователем
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/tasks/add_task``


* Запрос
  .. code-block::

     {
       collar_id: 321,
       template_id: 101,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block::

     {
       task_id: 201
     }
