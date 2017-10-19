crontab -r;
sudo pip uninstall vatan &&
python setup.py bdist_wheel &&
sudo pip install dist/vatan-0.1-py2-none-any.whl &&
rm -Rf ~/.vatan/

