# Fitness-Tracker-Api



Here is a full README for the project:


Fitness Tracker API
=====================

Overview
--------

This is a Django REST framework project that provides a Fitness Tracker API. The API allows users to manage their fitness activities by logging, updating, deleting, and viewing their activity history.

Features
--------

* **Activity Management**: Create, Read, Update, and Delete (CRUD) fitness activities.
* **User Management**: Create, Read, Update, and Delete (CRUD) users.
* **Activity History**: View activity history for a user.
* **Activity Metrics**: Calculate and return activity metrics for a user.
* **Optional Filters**: Filter activity history by date range or activity type.
* **Validation**: Validate required fields for activities and users.

Endpoints
--------

### Activity Endpoints

* `POST /api/activities/`: Create a new activity.
* `GET /api/activities/`: Get a list of all activities for a user.
* `GET /api/activities/{id}/`: Get a specific activity by ID.
* `PUT /api/activities/{id}/`: Update a specific activity by ID.
* `DELETE /api/activities/{id}/`: Delete a specific activity by ID.

### User Endpoints

* `POST /api/users/`: Create a new user.
* `GET /api/users/`: Get a list of all users.
* `GET /api/users/{id}/`: Get a specific user by ID.
* `PUT /api/users/{id}/`: Update a specific user by ID.
* `DELETE /api/users/{id}/`: Delete a specific user by ID.

### Activity History Endpoints

* `GET /api/users/{id}/history/`: Get activity history for a user.


Installation
------------

To install the project, follow these steps:

1. Clone the repository: `git clone https://github.com/bolajeee/fitness-tracker-api.git`
2. Install the requirements: `pip install -r requirements.txt`
3. Run the migrations: `python manage.py migrate`
4. Run the server: `python manage.py runserver`

API Documentation
-----------------

The API documentation can be found at `http://localhost:8000/api/docs/`.

Contributing
------------

Contributions are welcome! Please submit a pull request with your changes.

License
-------

This project is licensed under the MIT License.

Acknowledgments
---------------

* Django REST framework: https://www.django-rest-framework.org/
* Django: https://www.djangoproject.com/