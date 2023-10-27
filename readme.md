# zpi
<h1>
Zespołowe Przedsięwzięcie Informatyczne
</h1>

<h3>1. Docker</h3>
<h4>How to run</h4>
<p>
  In directory "../zpi/" run command "docker-compose up" <br>
  Django is running on address: http://127.0.0.1:8000/ <br>
  Frontend Angular is running on address: http://127.0.0.1:4200/ <br>
</p>

<h4>Build</h4>
<p>
    After updating requirements.txt remember to run docker-compose build
    to ensure that all project requirements are installed.
</p>

<h3>2. Migrations in django</h3>
<p> 
docker-compose exec django-app python manage.py makemigrations <br>
docker-compose exec django-app python manage.py  migrate
</p>

<h3>3. Populate DB with random data</h3>
<p> 
docker-compose exec django-app python populate_db.py <br>
</p>
