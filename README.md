# Videogames API

The videogames API provides you with information about Videogames, The Studios that created them, and it lets you list them by Category or by the Studio. It is the Capstone project of the Full Stack Nanodegree from Udacity.

There is a DEMO deployed on HEROKU (as part of the requirements on)

https://videogames-juanchete-udacity.herokuapp.com/


## Getting Started

In order to run it locally (development), you will need:

 * PostgreSQL Server running (with a user a password)
 * Python3 with a virtual enviroment configured 
 * Follow the instructions of this readme ;)

### Installing Dependencies

#### Python 3.7.6

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Follow the instructions in [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to create a Virtual enviroment, **or** the following instructions (Linux or WSL):

First install python3-venv
```bash
sudo apt-get install python3-venv
```
Then, create a virtual enviroment with the following command 
```bash
python3 -m venv env    
```
Activate the venv with:
```bash
source env/bin/activate
```

Now you can **install dependencies** in the Virtual Environment just created

Remember to add env folder and pip to .gitignore to avoid pushing it to the repository

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to communicate with the Database 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from the frontend server that you will develop if you really want to :) 

## Database Setup

With Postgres running, create a database called videogames, run the API to create the tables and relations, and after, put some data using the `videogames_data.psql` file provided.
From the root folder in terminal run:

```bash
sudo -u postgres createdb videogames
. setup.sh
psql videogames < videogames_data.psql
```

## Running the server

It is included a `setup.sh` script to set up the local variables needed for testing and production on your development.

To use it:
 * Activate your virtual environment if it is not activated (*source bin/env/activate*)
 * Import the variables in the running bash session
 ```bash
    $ . setup.sh
 ```
 * Execute `flask run`. It will put the API listening on localhost:5000

### Environment variables

-  The `setup.sh` file includes all needed variables, however you can change them to fit your enviroment

## Testing

We need the TOKENS for the different roles in our `setup.sh` so first, we enter into our Virtual Env, and import the setup.sh contents.

```bash
source env/bin/activate
. setup.sh
createdb videogames_test
psql videogames_test < videogames_test_data.sql
python test_api.py
```
**Note:** The tokens supplied will expire, hurry up before it occurrs or yours test will fail with 403 errors ;)

### Login Testing to obtain tokens

**ONLY FOR TESTING, you must disable this functionality when it evolves to a production system ;)**

You can simulate the Login process to register and obtain an access_token in the url:

http://127.0.0.1:5000/login

It will redirect you to the Auth0 Login page. After register or login, it redirects you to the login-details page. In this page you can copy the JWT generated for the user that has logged in.

If you want to logout, just click on logout and you will be out of the application.

### Postman collection for testing

In the `tests` folder you have two files:

* `capstone-videogames-test.HEROKU.postman_collection.json` - To test the API deployed on Heroku
* `capstone-videogames-test.LOCAL.postman_collection.json` - to test the API in local

Feel free to import it before the tokens expires!

## API Reference

### Getting Started

* Base URL: The API is launched by default on, http://127.0.0.1:5000/, but feel free to change the following variables to your needs in the `setup.sh`file:
 
  * FLASK_RUN_PORT is the port to listen requests
  * FLASK_RUN_HOST the hosts to listen request (i.e localhost, your Public IP or 0.0.0.0)

### Authentication:

The apps needs Authentication and it is granted by Auth0. There are 4 roles:

#### Public

An user that is not authenticated, can request / and /videogames only

#### User

An authenticated user, who can request videogames, categories, studios and videogames by category or studio with the following permissions:
```
get:categories
get:studios
get:videogames
```

#### Studio

An authenticated user of an Videogame Studio who can create, read, update and delete videogames, and modify info of a Studio. It has the following permissions in Auth0

``` 
delete:videogames
get:categories
get:studios
get:videogames
patch:studios
patch:videogames
post:videogames
``` 

#### Manager

An authenticated user with super cow powers. He/She can do everything in this API. The role Manager has the following permissions:
``` 
get:videogames
post:videogames
patch:videogames
delete:videogames
get:categories
post:categories
patch:categories
delete:categories
get:studios
post:studios
patch:studios
delete:studios

``` 

### Error Handling

Errors are returned as JSON objects in the following format.

```json
{
  "error": 404, 
  "message": "Resource not found", 
  "success": false
}
``` 
Authentication errors can have more details:

```json
{
  "error": 401, 
  "message": {
    "code": "UNAUTHORIZED", 
    "description": "No Authorization header supplied"
  }, 
  "success": false
}
```

The API will return different error types when a request fails:

400: Bad Request
401: Needs Auth
403: Forbidden (you need more permissions)
404: Resource Not Found
412: Precondition Failed. Studio or Manager supplied could not exists
422: Not Processable
500: Internal Server Error

### Videogames

**GET '/videogames'**

- Fetches a dictionary of videogames with their category, description, name and studio. Both Studio and Category for each Videogame are returned
- Request Arguments: if supplied `page=page_number` will paginate results
- Authentication: not required
- Role required: none

- Returns:
  - A Boolean if `success`
  - A return `code`
  - A page with the current `page` or `false` if no pagination was supplied on the request
  - A dictionary of `videogames` with their values
  - A number with the total of videogames
- Sample: `curl http://127.0.0.1:5000/videogames`
```json
{
  "code": 200, 
  "page": false,
  "success": true,
  "total_videogames": 1,
  "videogames": {
      "category": {
        "id": 1, 
        "name": "Motors"
      }, 
      "description": "Dummy description", 
      "id": 6, 
      "name": "Dummy Videogame", 
      "studio": {
        "id": 1, 
        "location": "Dummy Location Patched", 
        "name": "Dummy Name Patched"
      }
  },
}
```

**GET '/videogames/<videogame_id>'**

- Fetches a videogames with their category, description, name and studio. 
- Request Arguments: without arguments
- Authentication: not required
- Role required: none
- Returns:
  - A Boolean if `success`
  - A return `code`
  - A `videogame` object with its information or 404 if no videogame with the id supplied
- Sample: `curl -H "Authorization: Bearer $TOKEN_ROLE_USER" http://127.0.0.1:5000/videogames/<videogame_id>`
```json
{
  "code": 200, 
  "success": true,
  "videogame": {
      "category": {
        "id": 1, 
        "name": "Motors"
      }, 
      "description": "Dummy description", 
      "id": 6, 
      "name": "Dummy Videogame", 
      "studio": {
        "id": 1, 
        "location": "Dummy Location Patched", 
        "name": "Dummy Name Patched"
      }
  },
}
```
**POST '/videogames'**

- Create a new videogames from a supplied studio and category
- Request Arguments: JSON body with the mandatory fields
- Authentication: Requires Auth
- Role required: Studio or Manager
```json
{
    "name": "New Videogame",
    "description": "New description",
    "studio_id": 1,
    "category_id": 1
}
```
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The videogame object `created` with its information or an error
- Sample: `curl -X POST -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" -H 'Content-Type: application/json' -d '{"name": "New Videogame","description": "New description","studio_id": 1,"category_id": 1}' http://127.0.0.1:5000/videogames`
```json
{
    "code": 200,
    "created": {
        "category": {
            "id": 1,
            "name": "Motors"
        },
        "description": "New description",
        "id": 9,
        "name": "New Videogame",
        "studio": {
            "id": 1,
            "location": "Studio Location",
            "name": "Studio Name"
        }
    },
    "success": true
}
```
**PATCH '/videogames/<videogame_id>'**

- Updates value of a videogame
- Request Arguments: JSON body with the values to change, videogame_id in the request path
- Authentication: Requires Auth
- Role required: Studio or Manager
```json
{
    "name": "Updated Videogame Name",
    "description": "New description, but updated"
}
```
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The `updated` object
- Sample: `curl -X PATCH -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" -H 'Content-Type: application/json' -d '{"name": "Updated Videogame Name","description": New description, but updated"}' http://127.0.0.1:5000/videogames/<videogame_id>`

```json
{
    "code": 200,
    "success": true,
    "updated": {
        "category": {
            "id": 1,
            "name": "Motors"
        },
        "description": "New description, but updated",
        "id": 1,
        "name": "Updated Videogame Name",
        "studio": {
            "id": 1,
            "location": "Studio Location",
            "name": "Studio Name"
        }
    }
}
```

**DELETE '/videogames/<videogame_id>'**

- Deletes a videogame
- Request Arguments: videogame_id
- Authentication: Requires Auth
- Role required: Studio or Manager
```json
{
    "name": "Updated Videogame Name",
    "description": "New description, but updated"
}
```
- Returns:
  - A Boolean if `success`
  - A return `code`
  - A `deleted` key with de id of the deleted videogame
- Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN_ROLE_MANAGER" http://127.0.0.1:5000/videogames/<videogame_id>`
```json
{
    "code": 200,
    "deleted": 8,
    "success": true
}
```
### Categories

**GET '/categories'**

- Fetches a dictionary of categories. with id and name
- Request Arguments: None
- Authentication: Requires Auth
- Role required: User, Studio or Manager
- Returns:
  - A Boolean if `success`
  - A return `code`
  - A dictionary of `categories` with their values
  - A number with the total of categories
- Sample: `curl -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" http://127.0.0.1:5000/categories`
```json
{
    "categories": [
        {
            "id": 3,
            "name": "Rpg"
        },
        {
            "id": 4,
            "name": "Shooter"
        },
        {
            "id": 5,
            "name": "Dummy Category"
        },
        {
            "id": 6,
            "name": "Dummy Category"
        },
        {
            "id": 1,
            "name": "Motors"
        }
    ],
    "code": 200,
    "success": true,
    "total_categories": 5
}
```

**GET '/categories/<category_id>'**

- Fetches a category
- Request Arguments: ID of the category requested
- Authentication: Requires Auth
- Role required: User, Studio or Manager
- Returns:
  - A Boolean if `success`
  - A return `code`
  - A `category` object with its information or 404 if no category with the id supplied
- Sample: `curl -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" http://127.0.0.1:5000/categories/<category_id>`
```json
{
    "category": {
        "id": 1,
        "name": "Motors"
    },
    "code": 200,
    "success": true
}
```

**GET '/categories/<category_id>/videogames'**

- Fetches the videogames of the passed category
- Request Arguments: ID of the category, and optional a page param for pagination
- Authentication: Requires Auth
- Role required: User, Studio or Manager
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The `category` supplied
  - An array of `videogames`
  - The number of videogames for the category selected (for pagination)

- Sample: `curl -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" http://127.0.0.1:5000/categories/<category_id>/videogames`

```json
{
    "category": {
        "id": 1,
        "name": "Motors"
    },
    "code": 200,
    "success": true,
    "total_videogames": 5,
    "videogames": [
        {
            "category": {
                "id": 1,
                "name": "Motors"
            },
            "description": "Dummy description",
            "id": 6,
            "name": "Dummy Videogame",
            "studio": {
                "id": 1,
                "location": "Dummy Location Patched",
                "name": "Dummy Name Patched"
            }
        }
    ]
}
```

**POST '/categories'**

- Creates a new category 
- Request Arguments: JSON body with the category fields (name)
- Authentication: Requires Auth
- Role required: Manager

```json
{
    "name": "New Category",
}
```
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The category object named `created` with its information or an error
- Sample: `curl -X POST -H "Authorization: Bearer $TOKEN_ROLE_MANAGER" -H 'Content-Type: application/json' -d '{"name": "New Category"}' http://127.0.0.1:5000/categories`
```json
{
    "code": 200,
    "created": {
        "id": 7,
        "name": "New Category"
    },
    "success": true
}
```
**PATCH '/categories/<category_id>'**

- Updates value of a category
- Request Arguments: JSON body with the values to change, category_id in the request path
- Authentication: Requires Auth
- Role required: Manager
```json
{
    "name": "Updated Category Name",
}
```
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The `updated` object
- Sample: `curl -X PATCH -H "Authorization: Bearer $TOKEN_ROLE_USER" -H 'Content-Type: application/json' -d '{"name": "Updated Category Name"}' http://127.0.0.1:5000/categories/<category_id>`
```json
{
    "code": 200,
    "success": true,
    "updated": {
        "id": 7,
        "name": "Motors"
    }
}
```

**DELETE '/categories/<category_id>'**

- Deletes a Category
- Request Arguments: category_id
- Authentication: Requires Auth
- Role required: Manager
- Returns:
  - A Boolean if `success`
  - A return `code`
  - A `deleted` key with the id of the deleted category
- Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN_ROLE_MANAGER" http://127.0.0.1:5000/categories/<category_id>`

```json
{
    "code": 200,
    "deleted": 7,
    "success": true
}
```

### Studios

**GET '/studios'**

- Fetches a dictionary of studios. 
- Request Arguments: None
- Authentication: Requires Auth
- Role required: User, Studio or Manager
- Returns:
  - A Boolean if `success`
  - A return `code`
  - A dictionary of `studios` with their values
  - A number with the total of studios
- Sample: `curl -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" http://127.0.0.1:5000/studios`
```json
{
    "code": 200,
    "studios": [
        {
            "id": 3,
            "location": "Santa Monica",
            "name": "Activision"
        },
        {
            "id": 4,
            "location": "Tokyo",
            "name": "Square Enix"
        }
    ],
    "success": true,
    "total_studios": 2
```

**GET '/studios/<studio_id>'**

- Fetches a studio
- Request Arguments: ID of the studio requested
- Authentication: Requires Auth
- Role required: User, Studio or Manager
- Returns:
  - A Boolean if `success` 
  - A return `code`
  - A `studio` object with its information or 404 if no studio with the id supplied
- Sample: `curl -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" http://127.0.0.1:5000/studios/<studio_id>`
```json
{
    "code": 200,
    "studio": {
        "id": 1,
        "location": "Studio Location",
        "name": "Studio Name"
    },
    "success": true
}
```

**GET '/studios/<studio_id>/videogames'**

- Fetches the videogames of the passed studio
- Request Arguments: ID of the studio, and optional a page param for pagination
- Authentication: Requires Auth
- Role required: User, Studio or Manager
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The `studio` supplied
  - An array of `videogames`
  - The number of videogames for the studio selected (for pagination)
- Sample: `curl -H "Authorization: Bearer $TOKEN_ROLE_STUDIO" http://127.0.0.1:5000/studios/<studio_id>/videogames`

```json
{
    "code": 200,
    "studio": {
        "id": 1,
        "location": "Dummy Location Patched",
        "name": "Dummy Name Patched"
    },
    "success": true,
    "total_videogames": 13,
    "videogames": [
        {
            "category": {
                "id": 1,
                "name": "Motors"
            },
            "description": "Dummy description",
            "id": 6,
            "name": "Dummy Videogame",
            "studio": {
                "id": 1,
                "location": "Dummy Location Patched",
                "name": "Dummy Name Patched"
            }
        }
    ]
}
```

**POST '/studios'**

- Creates a new studio 
- Request Arguments: JSON body with the studio fields (name)
- Authentication: Requires Auth
- Role required: Manager

```json
{
    "name": "New Studio",
    "location":"New Studio Location"
}
```
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The studio object named `created` with its information or an error
- Sample: `curl -X POST -H "Authorization: Bearer $TOKEN_ROLE_USER" -H 'Content-Type: application/json' -d '{"name": "New Studio","location":"New Studio Location"}' http://127.0.0.1:5000/studios`

```json
{
    "code": 200,
    "created": {
        "id": 9,
        "location": "New Studio Location",
        "name": "New Studio"
    },
    "success": true
}
```
**PATCH '/studios/<studio_id>'**

- Updates value of a studio
- Request Arguments: JSON body with the values to change, studio_id in the request path
- Authentication: Requires Auth
- Role required: Studio or Manager
```json
{
    "name": "Updated Studio Name",
}
```
- Returns:
  - A Boolean if `success`
  - A return `code`
  - The `updated` object

```json
{
    "code": 200,
    "success": true,
    "updated": {
        "id": 7,
        "name": "Updated Studio Name",
        "location": "Not updated Location"
    }
}
```

**DELETE '/studios/<studio_id>'**

- Deletes a Studio
- Request Arguments: studio_id
- Authentication: Requires Auth
- Role required: Manager
- Returns:
  - A Boolean if `success`
  - A return `code`
  - A `deleted` key with the id of the deleted studio
- Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN_ROLE_MANAGER" http://127.0.0.1:5000/studios/<studio_id>`

```json
{
    "code": 200,
    "deleted": 2,
    "success": true
}
```

## Authors

Juan José Rodríguez Buleo

## Acknowledgements

Our Udacity Coaches and my family.