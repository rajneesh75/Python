from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data
users = [
    {"id": 1, "name": "Rajneesh"},
    {"id": 2, "name": "John"}
]


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    return jsonify(user) if user else ('User not found', 404)


@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    users.append(new_user)
    return jsonify(new_user), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
