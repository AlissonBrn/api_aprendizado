from flask import Flask, jsonify, request
import json

app = Flask(__name__)

USERS_FILE = 'users.json'

# Função auxiliar para carregar os usuários
def load_users():
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

# Função auxiliar para salvar os usuários
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Rota principal
@app.route('/')
def home():
    return "Bem-vindo à API de Usuários!"

# GET - Listar todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    users = load_users()
    return jsonify(users)

# POST - Adicionar novo usuário
@app.route('/users', methods=['POST'])
def add_user():
    users = load_users()
    data = request.get_json()

    if not data.get('name') or not data.get('email'):
        return jsonify({"error": "Nome e email são obrigatórios"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }

    users.append(new_user)
    save_users(users)
    return jsonify(new_user), 201

# GET - Buscar usuário por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuário não encontrado"}), 404

# DELETE - Remover usuário
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = load_users()
    new_users = [u for u in users if u['id'] != user_id]
    
    if len(users) == len(new_users):
        return jsonify({"error": "Usuário não encontrado"}), 404

    save_users(new_users)
    return jsonify({"message": "Usuário removido com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
