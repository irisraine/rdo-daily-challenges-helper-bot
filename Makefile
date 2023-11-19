install:
	poetry install
	
lint:
	poetry run flake8 engine

start:
	poetry run rdo-daily-challenges-helper-bot
