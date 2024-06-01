
Протокол приложения nursary-app
===============================

.. autosummary::
   :toctree: generated

users_router
------------

Вход в учётную запись
^^^^^^^^^^^^^^^^^^^^^

``/users/signin``


* Запрос
  .. code-block:: console

     {
       login: "user123",
       password: "superuser"
     }

* Ответ
  .. code-block:: console

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
  .. code-block:: console

     {
       login: "user123",
       password: "superuser",
       is_admin: true,
       admin_token: "admin_token"
     }

* Ответ
  .. code-block:: console

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
  .. code-block:: console

     {
       login: "user123",
       password: "superuser"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

Изменение логина и/или пароля учётной записи
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/users/change``


* Запрос
  .. code-block:: console

     {
       login: "user123",
       password: "superuser",
       new_login: "123user",
       new_password: "password"
     }

* Ответ
  .. code-block:: console

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
  .. code-block:: console

     {
       name: "Ralfy",
       location: "Irkutsk",
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       dog_id: 123
     }

Добавление в БД нового ошейника
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/collars/add_collar``


* Запрос
  .. code-block:: console

     {
       code: "123abc",
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       collar_id: 123
     }

Привязка ошейника к определённой собаке
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/collars/link``


* Запрос
  .. code-block:: console

     {
       collar_id: 123,
       dog_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

Удаление собаки из БД
^^^^^^^^^^^^^^^^^^^^^

``/collars/remove_dog``


* Запрос
  .. code-block:: console

     {
       dog_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

Удаление ошейника из БД
^^^^^^^^^^^^^^^^^^^^^^^

``/collars/remove_collar``


* Запрос
  .. code-block:: console

     {
       collar_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

Отвязка ошейника от определённой собаке
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/collars/unlink``


* Запрос
  .. code-block:: console

     {
       collar_id: 123,
       dog_id: 456,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

tasks_router
------------

Добавление нового задания пользователем
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/tasks/add_task``


* Запрос
  .. code-block:: console

     {
       collar_id: 321,
       text: "Всем привет, и сегодня вам нужно будет собаку!",
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       task_id: 201
     }

Размещение отклика на задание
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/tasks/add_response``


* Запрос
  .. code-block:: console

     {
       task_id: 321,
       image_path: https://host/images/answer.png,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       response_id: 201
     }

Подтверждение автором задания отклика на это задание
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``/tasks/confirm_response``


* Запрос
  .. code-block:: console

     {
       response_id: 321,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

Удаление задания
^^^^^^^^^^^^^^^^

Пользователь может удалять задания, на которые ещё нет ни одного ответа
``/tasks/remove_task``


* Запрос
  .. code-block:: console

     {
       task_id: 321,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

Удаление отклика
^^^^^^^^^^^^^^^^

``/tasks/remove_response``


* Запрос
  .. code-block:: console

     {
       response_id: 321,
       user_token: "QWE123RTY"
     }

* Ответ
  .. code-block:: console

     {
       success: true
     }

Получение заданий автора
^^^^^^^^^^^^^^^^^^^^^^^^

``/tasks/get_tasks``


* Запрос
  .. code-block:: console

     {
       author_id: 1,
     }

* 
  Ответ

  .. code-block:: console

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
