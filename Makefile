# Инициализирует миграции
start_migrate:
	flask db init
	flask db migrate -m "Initial migration."
	flask db upgrade

# Запускает сервер в режиме разработки с включенным дебаггером
run:
	flask run --debug