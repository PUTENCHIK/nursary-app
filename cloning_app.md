# Разворачивание приложения
## Linux

1. Создание директории для проекта и виртуального окружения:
```bash
mkdir nursary_app
cd nursary_app
mkdir venv
```
2. Установка необходимых пакетов:
```bash
sudo apt-get update
sudo apt-get install python3.10
sudo apt install python3-pip
```
3. Создание виртуального окружения и активация (опционально):
```bash
python3 -m venv venv/
source venv/bin/activate
```
4. Установка необходимых библиотек:
```bash
pip install "fastapi[all]" uvicorn sqlalchemy
pip install -U Werkzeug
```

