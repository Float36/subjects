# Flask Blog App

Веб‑додаток на Flask із авторизацією, постами, статичними ассетами й готовою Docker‑орієнтованою конфігурацією (uWSGI + Nginx + Postgres). Проєкт уже містить робочі налаштування для локального запуску як через Docker, так і напряму у віртуальному середовищі Python.

## Стек
- Flask 3, Jinja2, WTForms
- SQLAlchemy + Flask‑Migrate
- Flask‑Login, Flask‑Bcrypt
- Flask‑Assets (збирання CSS/JS)
- PostgreSQL
- uWSGI (в Docker), Nginx (reverse‑proxy в Docker)

## Структура проєкту (скорочено)
```
app/
  __init__.py           # create_app(), реєстрація blueprints, extensions, assets
  bundles.py            # Flask‑Assets bundles
  config.py             # конфіг, читає змінні середовища для БД
  extensions.py         # db, migrate, login_manager, assets
  routes/               # blueprints: user, post
  models/               # SQLAlchemy моделі
  templates/            # Jinja2 шаблони
  static/               # CSS, JS, зображення, upload
run.py                  # WSGI‑вхід (application = create_app())
app.ini                 # uWSGI конфіг (Docker)
Dockerfile              # образ застосунку
docker-compose.yml      # postgres + flask(uWSGI) + nginx
requirements.txt        # залежності Python
```

## Вимоги
- Docker і Docker Compose (для варіанту з контейнерами), або
- Python 3.12 (для локального запуску без Docker)
- PostgreSQL (для локального запуску без Docker)

## Швидкий старт (Docker, рекомендовано)
1. Створіть файл `.env` у корені проєкту:
```bash
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=coderfolder
POSTGRES_PASSWORD=coderfolder
POSTGRES_DB=mydb
```
2. Запустіть:
```bash
docker compose up -d --build
```
3. Відкрийте застосунок:
- http://localhost:8080

Примітки:
- Сервіс `postgres` публікується як `54321:5432` на хості. Додаток всередині мережі Docker звертається до `postgres:5432` (тому саме такі значення у `.env`).
- uWSGI слухає сокет/порт 8080, а Nginx проксіює HTTP на `localhost:8080` зовні.

Зупинити й видалити контейнери:
```bash
docker compose down
```

## Локальний запуск без Docker (WSL/Linux або Linux/macOS)
1. Підготуйте віртуальне середовище та залежності:
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
2. Розгорніть БД PostgreSQL і створіть базу:
```bash
createdb mydb            # або: psql -c "CREATE DATABASE mydb;"
```
3. Створіть `.env` у корені проєкту з параметрами доступу до БД:
```bash
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=coderfolder
POSTGRES_PASSWORD=coderfolder
POSTGRES_DB=mydb
```
4. Запуск у dev‑режимі (Flask):
```bash
export FLASK_APP=run:create_app
flask run --port 8080
```
Відкрийте `http://127.0.0.1:8080`.

Альтернатива: запуск через uWSGI без Nginx (HTTP‑режим):
```bash
uwsgi --http :8080 --wsgi-file run.py --callable application
```

> У `app/__init__.py` вже є `db.create_all()`, тож базові таблиці створяться автоматично під час першого запуску. Міграції Alembic можна додати пізніше за потреби.

## Змінні середовища
Читаються у `app/config.py`:
- `POSTGRES_HOST` (дефолт: `127.0.0.1`)
- `POSTGRES_PORT` (дефолт у коді: `5532`) — якщо ваш Postgres слухає стандартний порт, обовʼязково встановіть `5432` у `.env`.
- `POSTGRES_USER` (дефолт: `coderfolder`)
- `POSTGRES_PASSWORD` (дефолт: `coderfolder`)
- `POSTGRES_DB` (дефолт: `mydb`)

Приклад `.env` для Docker:
```bash
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=coderfolder
POSTGRES_PASSWORD=coderfolder
POSTGRES_DB=mydb
```
Приклад `.env` для локального запуску:
```bash
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=coderfolder
POSTGRES_PASSWORD=coderfolder
POSTGRES_DB=mydb
```

## Міграції (опційно)
Alembic уже встановлений, але стартовий код створює таблиці через `db.create_all()`. Якщо бажаєте керувати схемою через міграції:
```bash
flask db init        # один раз
flask db migrate -m "init"
flask db upgrade
```

## Статичні файли та assets
- Визначені bundles збираються через Flask‑Assets (`app/bundles.py`).
- Шлях завантажень: `app/static/upload/` (також монтується у Docker за допомогою volume).

## Типові проблеми
- Невірний порт Postgres: у конфігу за замовчуванням `5532`. Якщо база на `5432`, зафіксуйте це у `.env`.
- База не створена: створіть `mydb` або змініть `POSTGRES_DB`.
- uWSGI локально не віддає HTTP: запускайте через `flask run` або `uwsgi --http ...`.


