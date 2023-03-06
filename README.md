# Introduction
This project contains a Python Django application for running a quiz that has a special feature: questions that follow the ranking the stars concept. For these questions, the correct answer is not predetermined, but rather determined based on which answer is given most often.

# Setup
1. `git clone https://github.com/JaapNieland/quiz.git` 
2. Create a (virtual) environment with python3 and Django installed
3. Move to the directory of the project: `cd mysite`
4. Prepare for database creation: `python3 manage.py makemigrations`
5. Actually create database: `python3 manage.py migrate`
6. OPTIONAL: create superuser to use the admin panel: `python manage.py createsuperuser` 
7. Fasten seat belts and launch: `python manage.py runserver` 
