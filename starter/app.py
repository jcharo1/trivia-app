import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import setup_db, Question, Category, db

#test 
QUESTIONS_PER_PAGE = 10

# paginating questions
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # creates and configures app
    app = Flask(__name__)
    setup_db(app)
    
    # set up CORS with '*' origins
    CORS(app, resources={'/': {'origins': '*'}})

    # CORS headers to set access control 
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        # handles GET request for all categories
        # get all categories and add to dict
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        
        # if no categories abort 404
        if (len(categories_dict) == 0):
            abort(404)

        # return category to data view 
        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    @app.route('/questions')
    def retrieve_questions():
  
        # get all questions and paginate
        selection = Question.query.all()
        total_questions = len(selection)
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()

        # get all categories and add to dict
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        # abort 404 if no questions
        if (len(current_questions) == 0):
            abort(404)

        # return to data view
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict
            })

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        # handles DELETE requests for deleting a question by id
        try:
            # get question by id, use one_or_none to only turn one result
            # or call exception if none selected
            question = Question.query.filter_by(id=id).one_or_none()

            # abort if question not found
            if question is None:
                abort(404)

            # delete and return success message
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': id,
            })
            # abort if there's a problem deleting the question
        except BaseException:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def post_question():
        # load request body and data
        body = request.get_json()

        # if search term is present
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')

            # query the database using search term
            selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # 404 if no results found
            if (len(selection) == 0):
                abort(404)

            # paginate the results
            paginated = paginate_questions(request, selection)

            # return results
            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(Question.query.all())
            })
        # if no search term, create new question
        else:
            # load data from body
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_difficulty = body.get('difficulty')
            new_category = body.get('category')

            # ensure all fields have data
            if ((new_question is None) or (new_answer is None) or
                    (new_difficulty is None) or (new_category is None)):
                abort(422)

            # create and insert new question
            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category)

                question.insert()

                # get all questions and paginate
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'question_created': question.question,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })
            # abort 422 if exception
            except BaseException:
                abort(422)

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        # handles GET requests for getting questions based on category
        # gets category by id 
        category = Category.query.filter_by(id=id).one_or_none()
        # abort 400 if category not found
        if (category is None):
            abort(400)

        # get questions by category id 
        selection = Question.query.filter_by(category=category.id).all()

        # paginates selection 
        paginated = paginate_questions(request, selection)

        # returns results
        return jsonify({
            'success': True,
            'questions': paginated,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        # handles POST requests for play quiz
        try:
            body = request.get_json()

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            # If 'ALL' categories is 'clicked', filter available Qs
            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            # Filter available questions by chosen category & unused questions
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(
                        Question.id.notin_((previous_questions))).all()

            # randomly select next question from available questions
            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(
                    available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)

    # error handlers 
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    return app
app = create_app()
if __name__ == '__main__':
    app.run()
