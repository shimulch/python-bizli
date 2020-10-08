lint:
	poetry run isort bizli/**/*.py
	# stop the build if there are Python syntax errors or undefined names
	poetry run flake8 bizli/ --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	poetry run flake8 bizli/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test:
	poetry run coverage run -m pytest

test.dev:
	docker-compose up -d
	make test
	coverage html
	docker-compose down
