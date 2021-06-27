run-tests:
	pip install -r requirements_dev.txt;
	pytest --test-group-count 4 --test-group=$(STEP_NO) -n 4
