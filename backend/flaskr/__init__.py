import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(selection):
    page = request.args.get('page', 1, type=int)
    start = (page  - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app, resources={r"/http://127.0.0.1:5000/*": {"origins": "*"}})
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        
        # formatted_categories = [item.format() for item in category]
        # formatted_categories = [category.format() for category in categories]
        
        if len(categories)==0:
            abort(404)
        
        return{
            'success' : True,
            'categories': {category.id: category.type for category in categories},
            'total_categories': len(Category.query.all())
        }
            
    
    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        
        categories = Category.query.order_by(Category.id).all()
        # formatted_categories = [item.format() for item in categories]
        questions = Question.query.order_by(Question.id).all()
        current_question = paginate_questions(questions)
        
        if len(current_question)==0:
            abort(404)

        return {
            'success': True,
            'questions': current_question,
            'total_questions': len(Question.query.all()),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        }
    

    print(app.url_map)
    
    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id==question_id).one_or_none() 
            if question is None:
                abort(404)
            question.delete()
            return {
                'success': True
            }
        except:
            return{
                abort(422)
            }
    
    print(app.url_map)



    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()

        new_question = body.get("question", True)
        new_answer = body.get("answer", True)
        new_category = body.get("category", True)
        difficulty = body.get("difficulty", True)
        
        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=difficulty)
            question.insert()
            return {
                'success': True
            }
        
        except:
            abort(422)
                
            



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def search_question():
        body = request.get_json()
        search = body.get("search", None)
        
        questions = Question.query.order_by(Question.id).filter(
                    Question.title.ilike("%{}%".format(search))
        )
        current_question = paginate_questions(request, question)
        search_result = [question.format() for question in questions]

        return jsonify(
            {
                "questions": search_result,
                "total_question": len(questions.all()),
                'success': True,
                # 'questions': current_question,
                # 'total_questions': len(Question.query.all()),
                # 'categories': {category.id: category.type for category in categories},
                'current_category': None
            }
        )

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

