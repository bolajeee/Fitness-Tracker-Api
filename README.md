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
* **Authorization**: The API uses JSON Web Tokens (JWT) for authentication and authorization.

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

### Authorization Endpoints

* `POST /api/auth/login/`: Obtain a JWT token for a user.
* `POST /api/auth/refresh/`: Refresh a JWT token.

Authorization
------------

The API uses JSON Web Tokens (JWT) for authentication and authorization. To use the API, you need to obtain a JWT token by sending a `POST` request to the `/api/auth/login/` endpoint with your username and password. The token is then used in the `Authorization` header of subsequent requests.

Example:

```bash
curl -X POST \
  http://localhost:8000/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "your_username", "password": "your_password"}'
```

This will return a JWT token that can be used in subsequent requests:

```json
{
  "access": "your_jwt_token"
}
```

To use the token, include it in the `Authorization` header of your requests:

```bash
curl -X GET \
  http://localhost:8000/api/activities/ \
  -H 'Authorization: Bearer your_jwt_token'
```

Installation
------------

To install the project, follow these steps:

1. Clone the repository: `git clone https://github.com/bolajeee/fitness-tracker-api.git`
2. Install the requirements: `pip install -r requirements.txt`
3. Run the migrations: `python manage.py migrate`
4. Run the server: `python manage.py runserver`


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