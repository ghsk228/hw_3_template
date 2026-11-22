Запуск контейнера:

docker compose --env-file .env.example up -d --build

Команды общения с сервером:

curl http://localhost:8000/
curl -X POST http://localhost:8000/increment
curl -i http://localhost:8000/healthz
curl -i http://localhost:8000/readyz

Опустить сервер:

docker compose --env-file .env.example down

Поднять сервер:

docker compose --env-file .env.example up -d

Настройки

Переменная	По умолчанию	Значение
PORT	8000	Порт внутри контейнера; приложение слушает 0.0.0.0
GREETING	Hello, Docker!	Текст поля greeting
STORAGE	sqlite	sqlite для 4–6 баллов; redis для 8–10
DATA_FILE	/data/counter.db	Путь SQLite, используется только в режиме sqlite
REDIS_URL	redis://redis:6379/0	Адрес Redis, используется только в режиме redis
