import json
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
    # CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": ['http://localhost:5000', 'http://localhost:3000']}})
    
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
    

    # print(app.url_map)
    
    
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
    
    # print(app.url_map)



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

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        difficulty = body.get("difficulty", None)
        search = body.get("searchTerm", None)
        
        try:
            if search:
                
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))).all()
                # current_question = paginate_questions(questions)
                search_result = [question.format() for question in questions]

                return jsonify({
                    'success': True,
                    "questions": search_result,
                    "total_question": len(questions),
                    'current_category': None
                })
                
            else:
                
                
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
    # @app.route('/questions', methods=['POST'])
    # def search_question():
    #     body = request.get_json()
    #     search = body.get("searchTerm", None)
        
    #     questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))).all()
    #     current_question = paginate_questions(rquestions)
    #     search_result = [question.format() for question in questions]

    #     return jsonify({
    #         'success': True,
    #         "questions": current_question,
    #         "total_question": len(questions.all()),
    #         'current_category': None
    #     })
        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        questions = Question.query.order_by(Question.id).filter(Question.category==category_id).all()
        current_question = paginate_questions(questions)
        
        if len(current_question)==0:
            abort(404)

        return {
            'success': True,
            'questions': current_question,
            'total_questions': len(questions),
            'current_category': category_id
        }
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
    @app.route('/quizzes', methods=['POST'])
    def post_quiz():
        
        body = request.get_json()

        if not body:
            abort(400)
        
        # print(body)
        # print(body[2])
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        # print(previous_questions)
        # print(quiz_category)
        # print(quiz_category['id'])
        
        if previous_questions:
            if quiz_category['id']:
                question_list = (Question.query
                .filter(Question.category == str(quiz_category['id']))
                .filter(Question.id.notin_(previous_questions))
                .all())
            else:
                question_list = (Question.query
                .filter(Question.id.notin_(previous_questions))
                .all())
                
        else:
            if quiz_category['id']:
                question_list = (Question.query
                .filter(Question.category == str(quiz_category['id']))
                .all())
            else:
                question_list = (Question.query.all())
            
        # print(question_list)
        # print(previous_questions)
        
       
        # for item in question_list:
        #     # print(item)
        #     if item.id in previous_questions:
        #         del question_list[item]
            
                
        # questions_formatted = (question_list)
        # random_number = random.randint(0, len(question_list)-1)
        # random_question = question_list[random_number]
        # del question_list[random_number]
        i = 0
        while i <= len(question_list)-1:
            random_question = random.choice(question_list)
            i += 1
        # print(random_question)
        # print(question_list)
        
        if len(question_list) == 0:
            return{
                'success': True,
                'question': False
            }
        
        else:
            return jsonify({
                'success': True,
                'question': random_question.format()
            })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404
        
    @app.errorhandler(422)
    def unprocessable(error):
        return{
            'success': False,
            'error': 422,
            'message': 'Could not process request'
        },422

    @app.errorhandler(400)
    def bad_request(error):
        return{
            'success': False,
            'error': 400,
            'message': 'Bad Request, Make adjustment'
        },400
    
    @app.errorhandler(405)
    def not_allowed(error):
        return{
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }, 405
        
        
    @app.errorhandler(500)
    def internal_server_error(error):
        return{
            'success': False,
            'error': 500,
            'message': 'Server Currently Down'
        }, 500
    
    
    return app

