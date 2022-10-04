

refresh:
	rm -fr ./**/*__pycache*
	rm -fr ./**/migrations/0*.py
	rm -fr db.sqlite3
	python3 manage.py makemigrations && \
		python3 manage.py migrate && \
		python3 manage.py createsuperuser --username diercy --email diercy@gmail.com
