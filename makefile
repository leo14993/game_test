venv:
	@python3 -m venv .env;
	@source .env/bin/activate;
	@pip install --upgrade pip;

run:
	@echo ""
	@echo $(shell cat .env.example)
	@echo ""

	python main.py

test:
	@pytest
	@rm coverage.svg
	@coverage-badge -o coverage.svg