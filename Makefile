.DEFAULT_GOAL := test
NODE_BIN=./node_modules/.bin

.PHONY: clean compile_translations dummy_translations extract_translations fake_translations help html_coverage \
	migrate pull_translations push_translations quality requirements test update_translations validate

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  bundle                     build optimized JS bundle, compile CSS, and run collectstatic"
	@echo "  clean                      delete generated byte code and coverage reports"
	@echo "  compile_translations       compile translation files, outputting .po files for each supported language"
	@echo "  dummy_translations         generate dummy translation (.po) files"
	@echo "  extract_translations       extract strings to be translated, outputting .mo files"
	@echo "  fake_translations          generate and compile dummy translation files"
	@echo "  help                       display this help message"
	@echo "  html_coverage              generate and view HTML coverage report"
	@echo "  migrate                    apply database migrations"
	@echo "  pull_translations          pull translations from Transifex"
	@echo "  push_translations          push source translation files (.po) from Transifex"
	@echo "  quality                    run PEP8 and Pylint"
	@echo "  make accept                run acceptance tests"
	@echo "  requirements               install requirements for local development"
	@echo "  requirements.js            install JavaScript requirements for local development"
	@echo "  serve                      serve Programs at 0.0.0.0:8004"
	@echo "  static                     build and compress static assets"
	@echo "  test                       run tests and generate coverage report"
	@echo "  validate                   run tests and quality checks"
	@echo "  validate_js                run JavaScript unit tests and linting"
	@echo ""

clean:
	find . -name '*.pyc' -delete
	coverage erase
	rm -rf programs/assets programs/static/css programs/static/build coverage htmlcov

requirements.js:
	npm install
	$(NODE_BIN)/bower install

requirements: requirements.js
	pip install -qr requirements/local.txt --exists-action w

test: clean
	REUSE_DB=1 coverage run ./manage.py test programs --settings=programs.settings.test
	coverage report

quality:
	pep8 --config=.pep8 programs *.py acceptance_tests
	pylint --rcfile=pylintrc programs *.py acceptance_tests

static:
	$(NODE_BIN)/gulp css
	$(NODE_BIN)/r.js -o build.js
	python manage.py collectstatic --noinput -v0
	python manage.py compress -v0

serve:
	python manage.py runserver 0.0.0.0:8004

validate_js:
	rm -rf coverage
	$(NODE_BIN)/gulp test
	$(NODE_BIN)/gulp lint
	$(NODE_BIN)/gulp jscs

accept:
	nosetests --with-ignore-docstrings -v acceptance_tests

validate: test quality validate_js

migrate:
	python manage.py migrate

html_coverage:
	coverage html && open htmlcov/index.html

extract_translations:
	python manage.py makemessages -l en -v1 -d django
	python manage.py makemessages -l en -v1 -d djangojs

dummy_translations:
	cd programs && i18n_tool dummy

compile_translations:
	python manage.py compilemessages

fake_translations: extract_translations dummy_translations compile_translations

pull_translations:
	tx pull -a

push_translations:
	tx push -s
