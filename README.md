## Without-A-Hitch

**Platform:** Python 3

**Python Libraries required:**
* django 1.11
* psycopg2 2.7
* Pillow 4.2 (For images)

**External Dependencies:** Postgresql 9/10

#### **How to set up the environment to run the project:**
1. Install the necessary python libraries and postgresql
2. Create the database using configdb.sql
3. Run ```python manage.py makemigrations``` to create DB migrations from models
4. Run ```python manage.py migrate``` to create tables in the database from  models.py
5. Run ```python manage.py runserver``` to start the built in server
6. ~~Run ```python populate.py``` to populate the database with dummy data~~
