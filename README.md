# Song book

Setup Environment

    mkvirtualenv --python=/usr/bin/python3 song_book

Install Project

    git clone git clone git@bitbucket.org:sebaswilde/song_book.git
    cd song_book
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    python manage.py runserver --settings=song_book.settings.local
    
Fixtures for each Model

    python manage.py dumpdata root.<model_name> --indent 2 > fixtures/<model_name>.json
    python manage.py loaddata fixtures/*.json

Global Fixtures

    python manage.py dumpdata > backup.json
    python manage.py loaddata backup.json
    
Config Postgres

    sudo -u postgres psql;
    CREATE DATABASE song_book_db;
    CREATE USER song_book_user WITH PASSWORD 'song_book_pwd';
    GRANT ALL PRIVILEGES ON DATABASE song_book_db TO song_book_user;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO song_book_user;
    ALTER ROLE song_book_user SUPERUSER
    \q
    
Heroku update

    git add .
    git commit -m 'Commit message'
    git push heroku master

Heroku apply migrations
    
    heroku run bash
    Run commands
    exit(control + d)