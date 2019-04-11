#  Hacker news - GraphQL + Django

Setup Environment

    mkvirtualenv --python=/usr/bin/python3 hackernews

Install Project

    git clone https://github.com/SebasWilde/hackernews.git
    cd hackernews
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
