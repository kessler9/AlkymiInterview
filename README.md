# AlkymiInterview

<h1>Launch Process</h1>

If you don't already have virtualenv installed, run:

`python3 -m pip install --user virtualenv`

Then create your virtual environment:

`python3 -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt` 

`cd AlkymiInterview`

`python manage.py migrate`

`python manage.py runserver`

In a second terminal window:

`redis-server`

And in a third terminal window:

`source env/bin/activate`

`cd AlkymiInterview`

`celery -A AlkymiInterview worker -l info -B`

Now the celery, redis and the django development server are running.

use the following command to create a user for yourself:

`source env/bin/activate`

`cd AlkymiInterview`

`python manage.py createsuperuser`

Now would be a good time to take a look at the dynamic documentation.  Navigate to http://127.0.0.1:8000/docs/ to checkout the API
 
you can fetch a token through the API documentation's implementation of `POST api-token-auth/`

I couldn't find a way to get the api documentation to upload a file for the csv endpoint,
but the script test_upload.sh in AlkymiInterview can be used with the token to trigger the process, or postman
can be used with headers

`Authorization: Token <token from api-token-auth>`

and a binary file attachment of the csv

