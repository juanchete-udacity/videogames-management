# Videogames API

The videogames API provides you with information about Videogames, The Studios that created them, and it lets you list them by Category or by the Studio. It is the Capstone project of the Full Stack Nanodegree from Udacity.

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

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

With Postgres running, create a database called videogames, and put some data using the `videogames_data.psql` file provided.
From the root folder in terminal run:
```bash
sudo -u postgres createdb videogames
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

We need the TOKENS for the different roles in our `setup.sh` so first,  we enter our Virtual Env, and import the setup.sh contents
```bash
source env/bin/activate
. setup.sh
createdb videogames_test
psql videogames_test < videogames_test_data.sql
python test_api.py
```
**Note:** The tokens supplied will expire, hurry up before it occurrs or yours test will fail with 403 errors ;)

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

An authenticated user, who can request videogames, categories, studios and videogames by category or studio

#### Studio

An authenticated user of an Videogame Studio who can create, read, update and delete videogames, and modify info of a Studio

#### Manager

An authenticated user with super cow powers. He/She can do everything in this API

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
422: Not Processable
500: Internal Server Error

**GET '/videogames'**

- Fetches a dictionary of videogames with their category, description, name and studio. Both Studio and Category for each Videogame are returned
- Request Arguments: if supplied `page=page_number` will paginate results 
- Returns:
  - A Boolean if success
  - A return code
  - A page with the current page or `false` if no pagination was supplied on the request
  - A dictionary of videogames with their values
  - A number with the total of videogames
- Sample: `curl http://127.0.0.1:5000/videogames`
```json
{
  "code": 200, 
  "page": false,
  "success": true,
  "total_videogames": 1
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

**GET '/questions'**
- Fetches a list of paginated questions, with their ids, answer, category and difficulty.
- Request Arguments: *page*, with the number of pagination (established in the `QUESTIONS_PER_PAGE` variable in __init__.py)
- Returns:
  - A Dictionary of categories, with ids and texts
  - An integer with the current category
  - The list of questions
  - The total amount of questions 
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
```json
{
  "success": true,
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "ALL", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "total_questions": 19
```

**DELETE /questions/{question_id}**
Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend.

- Request Arguments: None, question_id is given in the path. *page* if given from the list view for pagination
- Returns: the id of the deleted question, the questions array, the number of questions remaining and the status  
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1?page=2`
```json

{
    "questions": [
        {
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "deleted": 16,
    "success": true,
    "total_questions": 15
}
```

**POST /questions**
Creates a new question with the body containing the fields of a question, or if search term was given, searches the question table for questions containing the term supplied

- Request Arguments: *body* with the following structure

    ```json
    {
        "question": "Question text",
        "answer": "Answer text",
        "difficulty": 1,
        "category": "4",
        "searchTerm": "search term"
    }
    ```

- Returns:
  - A json with the status of success, the question created, a dictionary of all the questions and the number of total questions.
  - Sample: `curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/questions -d '{"question": "question text", "answer": "answer", "difficulty": "1", "category": "1"}'`
    ```json
    {
        "success": true,
        "created": {"the question created"},
        "questions": "...",
        "total_questions": 16
    }
    ```

**GET {/categories/<category_id>/questions}**
Retrieves the questions with the category id passed as part of the path

- Request Arguments: *page* for pagination
- Returns: the dictionary of categories, the current category type, a list of questions as the result of the query and the total number of questions for pagination
- Sample: `curl http://127.0.0.1:5000/categories/1/questions?page=1`
```json

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "total_questions": 3,
  "success": true,
}
```

**POST /quizzes**

Retrieves a random question from the pool of questions or from the selected category (if any)

- Required Arguments: *body* with the following content:

```json
    {
        "previous_questions": [1,2,3],
        "quiz_category": {"type": "category type", "id": 1}
    }
```

- Returns: A JSON with the status of success and the question that is going to be asked

```json
    {
        "success": true,
        "question": {"the question"},
    }  
```
- Sample: `curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/quizzes -d '{"previous_questions": [1,11,13],"quiz_category": {"type": "category type", "id": "1"}}'` 
## Authors

Juan José Rodríguez Buleo

## Acknowledgements

Our Udacity Coaches and my family.