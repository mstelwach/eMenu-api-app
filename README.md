# eMenu-api-app

Design and implementation of an independent eMenu website. \
The eMenu serves as an online restaurant menu card.

## Want to use this project?
Uses the default Django development server.

  1. Build the images and run the containers. Spin up the containers:
  
        ```
        $ docker-compose up -d --build
        ```
  2. Perform your first migration:
        ```
        $ docker-compose exec web python manage.py makemigrations
        ```
        ```
        $ docker-compose exec web python manage.py migrate
        ```
  3. Load example data:
        ```
        $ docker-compose exec web python manage.py loaddata dishes.json
        ```
     <sub><sup>The file `dishes.json` must be loaded first.</sup></sub>
        ```
        $ docker-compose exec web python manage.py loaddata cards.json
        ```
  4. Create superuser:
        ```
        $ docker-compose exec web python manage.py createsuperuser
        ```
  5. Unit Tests:
        ```
        $ docker-compose exec web python manage.py test
        ```
     
Test it out at http://localhost:8000. \
The "backend" folder is mounted into the container and your code changes apply automatically.

####Open the logs associated with the celery service to see the tasks running periodically:

```
$ docker-compose logs -f 'celery'
```

#### Non-public API Functions:
1. REST API for menu management
2. Possibility to create multiple versions of cards (menu) with a unique name
3. Each card can contain any number of dishes
4. API is protected against unauthorized access (after user authorization)

#### Public API Functions:
1. Rest API for viewing non-empty menu card
2. Card detail showing all the card information and dishes in the card
3. Option to sort the list by name and number of dishes, using GET parameters (key=`ordering`, value=(`name`, `dishes_count`)
4. Filtering the list by name and period of addition and last update
  - `start_created`: filtering from date added (include)
  - `end_created`: filtering to date added (include)
  - `start_updated`: filtering from date updated (include)
  - `end_updated`: filtering to date updated (include)
  - `name`: filtering by name



#### Reporting
A mechanism that sends an e-mail to all users of the application once a day at 10:00. \
The e-mail contains information about the dishes added and modified from yesterday.

##### If you want to use Swagger to document the API:
http://localhost:8000/swagger

##### Tools to run the application::
* [docker] - https://www.docker.com/get-started