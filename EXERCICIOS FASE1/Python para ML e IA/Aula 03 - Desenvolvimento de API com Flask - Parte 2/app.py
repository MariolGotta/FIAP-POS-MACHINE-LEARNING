from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)

print(app.config['SECRET_KEY'])
print(app.config['SQLALCHEMY_DATABASE_URI'])
print(app.config['SWAGGER'])
print(app.config['CACHE_TYPE'])


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    time_minutes = db.Column(db.Integer, nullable=False)


@app.route('/register', methods=['POST'])
def register_user():
    """
    Registra um novo usuário.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Usuário já existe
    """
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Realiza o login e retorna um token de acesso.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Login realizado com sucesso, token retornado
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        token = create_access_token(identity=str(user.id))
        return jsonify({"acess token": token}), 201
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Rota protegida por autenticação JWT.
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Acesso autorizado
    """
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Usuário com ID {current_user_id} acessou a rota protegida"}), 200


@app.route('/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    """
    Cria uma nova receita.
    ---
    security:
      - Bearer: []
    parameters:
      - in: body
        name: recipe
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            ingredients:
              type: string
            time_minutes:
              type: integer
    responses:
      201:
        description: Receita criada com sucesso
    """
    data = request.get_json()
    new_recipe = Recipe(
        title=data['title'],
        ingredients=data['ingredients'],
        time_minutes=data['time_minutes']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"msg": "Recipe Created"}), 201


@app.route('/recipes', methods=['GET'])
def get_recipes():
    """
    Retorna uma lista de receitas com filtros opcionais.
    ---
    parameters:
      - in: query
        name: ingredients
        type: string
        required: false
        description: Filtrar por ingrediente
      - in: query
        name: max_time
        type: integer
        required: false
        description: Tempo máximo de preparo
    responses:
      200:
        description: Lista de receitas
    """
    ingredient = request.args.get("ingredients")
    max_time = request.args.get('max_time', type=int)

    query = Recipe.query
    if ingredient:
        query = query.filter(Recipe.ingredients.ilike(f'%{ingredient}%'))
    if max_time is not None:
        query = query.filter(Recipe.time_minutes <= max_time)

    recipes = query.all()
    return jsonify([
        {
            "id": r.id,
            "title": r.title,
            "ingredients": r.ingredients,
            "time_minutes": r.time_minutes
        }
        for r in recipes
    ])


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    """
    Atualiza uma receita existente.
    ---
    security:
      - Bearer: []
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
        description: ID da receita
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            ingredients:
              type: string
            time_minutes:
              type: integer
    responses:
      200:
        description: Receita atualizada com sucesso
    """
    data = request.get_json()
    recipe = Recipe.query.get_or_404(recipe_id)
    if 'title' in data:
        recipe.title = data['title']
    if 'ingredients' in data:
        recipe.ingredients = data['ingredients']
    if 'time_minutes' in data:
        recipe.time_minutes = data['time_minutes']
    db.session.commit()
    return jsonify({"msg": "Recipe updated"}), 200


@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    """
    Deleta uma receita.
    ---
    security:
      - Bearer: []
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
        description: ID da receita a ser deletada
    responses:
      200:
        description: Receita deletada com sucesso
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"msg": "Recipe deleted"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Banco de dados criado com sucesso!')
    app.run(debug=True)
