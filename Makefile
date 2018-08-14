HOST=127.0.0.1
TEST_PATH=./tests
RECIPEPREFIX= # prefix char is a space, on purpose; do not delete
PHONY=clean



clean: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +


install-deps:
	pipenv install


regen:
	PYTHONPATH=. pipenv run routegen -e lisnr.yaml > sns_lisnr.py


spinup:
	pipenv run  python sns_lisnr.py --configfile lisnr.yaml



