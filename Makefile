clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name __pycache__ -delete
	
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean: clean-pyc clean-build
	rm -Rf ~/.vatan/
	crontab -r
	
install:
	python setup.py bdist_wheel
	sudo pip install dist/vatan-0.1-py2-none-any.whl

uninstall:
	sudo pip uninstall vatan
