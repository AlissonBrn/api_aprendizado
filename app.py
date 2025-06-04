from flask import Flask, request, jsonify
from models import db, Tarefa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria o banco na primeira vez em que é acessado
@app.before_first_request
def criar_banco():
    db.create_all()

@app.route('/')
def home():
    return "API de Tarefas funcionando!"

# Criar nova tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()
    nova = Tarefa(
        titulo=dados['titulo'],
        descricao=dados.get('descricao', ''),
        concluida=dados.get('concluida', False)
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Tarefa criada!", "id": nova.id}), 201

# Listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = Tarefa.query.all()
    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "descricao": t.descricao,
            "concluida": t.concluida
        } for t in tarefas
    ])

# Obter uma tarefa por ID
@app.route('/tarefas/<int:id>', methods=['GET'])
def obter_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    return jsonify({
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": tarefa.concluida
    })

# Atualizar uma tarefa
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.descricao = dados.get('descricao', tarefa.descricao)
    tarefa.concluida = dados.get('concluida', tarefa.concluida)
    db.session.commit()
    return jsonify({"mensagem": "Tarefa atualizada!"})

# Deletar uma tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({"mensagem": "Tarefa deletada com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
