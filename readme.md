# zpi
Zespołowe Przedsięwzięcie Informatyczne


<h3>1. Running docker image</h3>
<p>
  In directory "../zpi/" run command "docker-compse up -d" <br>
  Django is running on address: http://127.0.0.1:8000/ <br>
  Frontend Angular is running on address: http://127.0.0.1:4200/ <br>
</p>

<h3> 2. Migrations in django</h3>
<p> 
docker-compose exec web python manage.py makemigrations <br>
docker-compose exec web python manage.py  migrate
</p>
