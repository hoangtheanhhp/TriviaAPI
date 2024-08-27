from flask import request, jsonify
from bson import ObjectId
from .models import question_serializer
import json

def init_routes(app, mongo):
    questions_collection = mongo.db.questions

    @app.route('/questions', methods=['GET'])
    def list_questions():
        # Get filter parameters from the request
        category = request.args.get('category')
        status = request.args.get('status')
        limit = request.args.get('limit', default=10, type=int)

        # Build the query filter
        query = {}
        if category:
            query['category'] = category
        if status:
            query['status'] = int(status)

        # Fetch questions from MongoDB with the filter
        questions = questions_collection.find(query).limit(limit)
        return jsonify([question_serializer(question) for question in questions])

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            question = request.json
            question['status'] = 1  # Mark new questions with status "NEW" (Code 1)
            questions_collection.insert_one(question)
            app.logger.info('Question added: %s', question)
            return jsonify({"message": "Question added successfully!"}), 201
        except Exception as e:
            app.logger.error('Error adding question: %s', str(e))
            return jsonify({"error": "Failed to add question"}), 500

    @app.route('/questions/<id>', methods=['PUT'])
    def edit_question(id):
        try:
            data = request.json
            questions_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            app.logger.info('Question updated: %s', data)
            return jsonify({"message": "Question updated successfully!"})
        except Exception as e:
            app.logger.error('Error updating question: %s', str(e))
            return jsonify({"error": "Failed to update question"}), 500

    @app.route('/questions/upload', methods=['POST'])
    def upload_questions():
        try:
            file = request.files['file']
            if file and file.filename.endswith('.json'):
                questions = json.load(file)
                for question in questions:
                    question['status'] = 1  # Mark new questions with status "NEW" (Code 1)
                questions_collection.insert_many(questions)
                app.logger.info('Questions uploaded from file: %s', file.filename)
                return jsonify({"message": "Questions uploaded successfully!"}), 201
            app.logger.warning('Invalid file format uploaded: %s', file.filename)
            return jsonify({"error": "Invalid file format. Please upload a JSON file."}), 400
        except Exception as e:
            app.logger.error('Error uploading questions: %s', str(e))
            return jsonify({"error": "Failed to upload questions"}), 500

    @app.route('/questions/<id>/delete', methods=['PUT'])
    def delete_question(id):
        try:
            questions_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": 0}})  # Mark question as deleted (status 0)
            app.logger.info('Question marked as deleted: %s', id)
            return jsonify({"message": "Question marked as deleted!"})
        except Exception as e:
            app.logger.error('Error marking question as deleted: %s', str(e))
            return jsonify({"error": "Failed to mark question as deleted"}), 500
