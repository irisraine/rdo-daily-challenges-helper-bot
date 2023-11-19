install:
	poetry install
	
lint:
	poetry run flake8 engine

start:
	poetry run rdo-daily-challenge-helper-bot
