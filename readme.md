# zpi
Zespołowe Przedsięwzięcie Informatyczne


<h3>1. Running docker image</h3>
<p>
  In directory "../zpi/" run command "docker-compse up" <br>
  Django is running on address: http://0.0.0.0:8000/ <br>
</p>

<h3> 2. Migrations in django</h3>
<p> 
docker-compose exec web python manage.py makemigrations <br>
docker-compose exec web python manage.py  migrate
</p>
