rm -rf instance/
mkdir instance
touch instance/app.db
python3 manage.py db create_all