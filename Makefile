.DEFAULT_GOAL := test

check_prereqs:
	bash -c '[[ -n $${VIRTUAL_ENV:-$${CONDA_PREFIX}} ]]'
	bash -c '[[ $$(python3 --version 2>&1) == *3.4.3* ]]'

install: check_prereqs
	python3 -m pip install -e '.[dev]'

test: install
	pylint singer -d missing-docstring,broad-except,bare-except,too-many-return-statements,too-many-branches,too-many-arguments,no-else-return,too-few-public-methods,fixme,protected-access
	nosetests -v
