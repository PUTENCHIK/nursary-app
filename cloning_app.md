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
sudo apt install python3.10-venv
```

3. Создание виртуального окружения и активация (опционально):
```bash
python3 -m venv venv/
source venv/bin/activate
```

4. Установка необходимых библиотек:
```bash
pip install "fastapi[all]" sqlalchemy
pip install -U Werkzeug
```

5. Клонирования проекта с GitHub:
```bash
git clone -b master https://github.com/PUTENCHIK/nursery-app.git
cd nursery-app
```
