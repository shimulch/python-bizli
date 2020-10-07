lint:
	isort bizli/**/*.py
	flake8 bizli/

test:
	docker-compose up -d
	pytest
	docker-compose down
