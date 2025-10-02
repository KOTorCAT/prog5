# Python Glossary API

REST API для управления глоссарием терминов Python с поддержкой CRUD-операций.

##  Функционал

- `GET /terms` — список всех терминов
- `GET /terms/{term}` — получить определение термина
- `POST /terms` — добавить новый термин
- `PUT /terms/{term}` — обновить определение
- `DELETE /terms/{term}` — удалить термин

Данные хранятся в SQLite. При старте создаются таблицы автоматически.

##  Запуск с Docker

```bash
docker build -t python-glossary-api .
docker run -p 8000:8000 python-glossary-api