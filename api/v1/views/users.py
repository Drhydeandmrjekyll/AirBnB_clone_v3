#!/usr/bin/python3
'''
Create new view for User objects - handles all default RESTful API actions
'''

# Import necessary modules
from flask import abort, jsonify, request
# Import User model
from models.user import User
from api.v1.views import app_views
from models import storage


# Route for retrieving all User objects
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''
    retrieves list of all User objects
    '''
    # Get all User objects from storage and convert them to dictionaries
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


# Route for retrieving a specific User object by ID
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''
    Retrieves User object
    '''
    # Get User object with given ID from storage
    user = storage.get(User, user_id)
    if user:
        # Return User object in JSON format
        return jsonify(user.to_dict())
    else:
        # Return 404 error if User object is not found
        abort(404)


# Route for deleting specific User object by ID
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''
    Deletes User object
    '''
    # Get User object with given ID from storage
    user = storage.get(User, user_id)
    if user:
        # Delete User object from storage and save changes
        storage.delete(user)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if User object is not found
        abort(404)

# Route for creating new User object
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    Creates User object
    '''
    # Check if request data is in JSON format
    if not request.get_json():
        # Return 400 error if request data is not in JSON format
        abort(400, 'Not a JSON')

    # Get JSON data from request
    data = request.get_json()
    if 'email' not in data:
        # Return 400 error if 'email' key is missing in JSON data
        abort(400, 'Missing email')
    if 'password' not in data:
        # Return 400 error if 'password' key is missing in JSON data
        abort(400, 'Missing password')

    # Create new User object with JSON data
    user = User(**data)
    # Save User object to storage
    user.save()
    # Return newly created User object in JSON format with 201 status code
    return jsonify(user.to_dict()), 201


# Route for updating an existing User object by ID
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    Updates User object
    '''
    # Get User object with given ID from storage
    user = storage.get(User, user_id)
    if user:
        # Check if request data is in JSON format
        if not request.get_json():
            # Return 400 error if request data is not in JSON format
            abort(400, 'Not a JSON')

        # Get JSON data from request
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        # Update attributes of User object with JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        # Save updated User object to storage
        user.save()
        # Return updated User object in JSON format with 200 status code
        return jsonify(user.to_dict()), 200
    else:
        # Return 404 error if User object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    Returns 404: Not Found
    '''
    # Return JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Return Bad Request message for illegal requests to the API
    '''
    # Return JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
