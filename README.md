# API Development and Documentation Final Project

## Trivia App

Trivia app is a web application that allows people to hold trivia on a regular basis using a webpage to manage the trivia app and play the game. This web application allow users to play the trivia game for six different categories Science, Art, Geography, History, Entertainment, Sports. It display to the user the total scores at the end of the game.

The application does the following:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

The trivia app was designed to helps solidify my ability to structure plan implement, and test an API - skills essential for enabling your future applications to communicate with others.

### GETTING STARTED
### Backend Setup
#### Install Dependencies
1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

#### Run the Server

From within the backend directory

To run the server, execute:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

#### Testing
To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### FrontEnd Setup

#### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

#### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```


## API REFERENCE

### GETTING STARTED
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. The frontend is hosted at the default, `http://127.0.0.1:5000`
- Authentication: This version of the application does not require authentication or API keys

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines. Other requirements for the project can be found in requirements.txt file in ./backend/requirements.txt


### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request, Make adjustment
- 404: Resource Not Found
- 422: Could not process request
- 405: Method Not Allowed
- 500: Server Currently Down



### Endpoints 
#### GET /categories
- General:
    - Returns a list of categories, success value, and total number of categories
    Sample: curl http://127.0.0.1:5000/categories
        {
            "categories": {
                "1": "Science",       
                "2": "Art",
                "3": "Geography",     
                "4": "History",       
                "5": "Entertainment", 
                "6": "Sports"
            },
            "success": true,        
            "total_categories": 6   
        }

#### GET /questions
- General:
    - Returns a list of questions, success value, total number of questions, list of question categories, and a current category
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    Sample: curl http://127.0.0.1:5000/questions
        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "current_category": null,
            "questions": [
                {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"   
                },
                {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
                },
                {
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                "answer": "George Washington Carver",
                "category": 4,
                "difficulty": 2,
                "id": 12,
                "question": "Who invented Peanut Butter?"
                },
                {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?"
                },
                {
                "answer": "One",
                "category": 2,
                "difficulty": 4,
                "id": 18,
                "question": "How many paintings did Van Gogh sell in his lifetime?"
                }
            ],
            "success": true,
            "total_questions": 19
        }

#### GET /categories/<int:category_id>/questions
- General:
    - Returns current category, a list of questions for that category, success value, and the total number of questions in the category
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    Sample: crul http://127.0.0.1:5000/categories/2/questions
        {
            "current_category": 2, 
            "questions": [
                {
                "answer": "One",
                "category": 2,
                "difficulty": 4,
                "id": 18,
                "question": "How many paintings did Van Gogh sell in his lifetime?"
                },
                {
                "answer": "Jackson Pollock",
                "category": 2,
                "difficulty": 2,
                "id": 19,
                "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"       
                }
            ],
            "success": true,
            "total_questions": 2
        }

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns only a success value.
    Sample: curl -X POST -H "Content-Type: application/json" -d '{"question":"Whom did Albert Einstein call the father of modern science?", "answer":"Galieo Galilei", "difficulty":"3", "category":"1"}' http://127.0.0.1:5000/questions
        {
        "success": true
        }

#### POST /questions
- General:
    - Returns a list of question that has the search substring, a success value, and the total number of questions in the search list
    Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "What"}'
        {
            "current_category": null, 
            "questions": [
                {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"   
                },
                {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
                },
                {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?"
                },
                {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
                },
                {
                "answer": "2007",
                "category": 4,
                "difficulty": 4,
                "id": 30,
                "question": "What year was the very first model of the iPhone released?"
                },
                {
                "answer": "Pierre Omidyar",
                "category": 4,
                "difficulty": 5,
                "id": 31,
                "question": "What is the name of the man who launched eBay back in 1995?"
                },
                {
                "answer": "2007",
                "category": 4,
                "difficulty": 3,
                "id": 34,
                "question": "What year was the very first model of the iPhone released?"
                }
            ],
            "success": true,
            "total_question": 9
        }

#### POST /quizzes
- General:
    - Takes the category and previous questions in the request. Return a single random question not in previous questions and a success value.
    Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [27, 20], "quiz_category": {"type": "Science", "id": "1"}}'
        {
            "question": {
                "answer": "1",
                "category": 1,
                "difficulty": 5,
                "id": 29,
                "question": "How many minutes does a blood cell take to do a circuit of the body?"
            },
            "success": true
        }

#### DELETE /questions/<int:question_id>
    - General:
        - Deletes the question of the given ID if it exists. Returns a success value.
        Sample: curl -X DELETE http://127.0.0.1:5000/questions/33
            {
            "success": true
        } 


## Deployment N/A

## Authors
    - Bamigboye Abiola: Work on the API and test suite to integrate with frontend
    - Udacity: Provided the frontend and starter kit for the project 

## Acknowledgements 
The awesome team at Udacity and all of my cohorts - especially Tony Baidoo.
