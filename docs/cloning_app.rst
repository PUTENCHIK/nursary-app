
Разворачивание приложения
=========================


#. 
   Создание директории для проекта и виртуального окружения:

   .. code-block:: bash

      mkdir nursary_app
      cd nursary_app
      mkdir venv

#. 
   Установка необходимых пакетов:

   .. code-block:: bash

      sudo apt-get update
      sudo apt-get install python3.10
      sudo apt install python3-pip
      sudo apt install python3.10-venv

#. 
   Создание виртуального окружения и активация (опционально):

   .. code-block:: bash

      python3 -m venv venv/
      source venv/bin/activate

#. 
   Установка необходимых библиотек:

   .. code-block:: bash

      pip install "fastapi[all]" sqlalchemy
      pip install -U Werkzeug

#. 
   Клонирования проекта с GitHub:

   .. code-block:: bash

      git clone -b master https://github.com/PUTENCHIK/nursery-app.git
      cd nursery-app

#. 
   Запуск приложения:


* С помощью Python-скрипта:
  .. code-block:: python

     python3 run.py

* Или используя uvicorn:
  .. code-block:: bash

     sudo apt install uvicorn
     uvicorn main:app --reload --port 5000 --host 0.0.0.0
