from flask import Flask, request, jsonify
import json
import datetime


app = Flask(__name__)
NOME_ARQUIVO = 'dados.json'

def ler_tarefas():
    try:
        with open(NOME_ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def escrever_tarefas_no_arquivo(tarefas):
    with open(NOME_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)


@app.route('/tarefas', methods= ['POST'] )
def def_create():
    dados_recebidos = request.get_json()

    if not dados_recebidos or 'titulo' not in dados_recebidos or 'descricao' not in dados_recebidos:
        return jsonify({"erro": "Os campos 'titulo' e 'descricao' são obrigatórios"}), 400

    list_tarefas = ler_tarefas()
    next_ID = max([tarefa.get('id', 0) for tarefa in list_tarefas]) + 1 if list_tarefas else 1

    agora = datetime.datetime.now()

    nova_tarefa = {
        "id": next_ID,
        "titulo": dados_recebidos['titulo'],
        "decricao": dados_recebidos['descricao'],
        'status': 'pendente',
        'data': agora.strftime('%d/%m/%Y %H:%M:%S')
    }
    list_tarefas.append(nova_tarefa)
    escrever_tarefas_no_arquivo(list_tarefas)
    return jsonify(nova_tarefa), 201

@app.route('/tarefas', methods=['GET'])
def listar_todas_as_tarefas():
    list_tarefas = ler_tarefas()
    return jsonify(list_tarefas)

@app.route('/tarefas/<int:id>', methods=['GET'])
def busca_tarefa(id):
    list_tarefas = ler_tarefas()
    for tarefa in list_tarefas:
        if tarefa.get('id') == id:
            return jsonify(tarefa)
    return jsonify({"erro": f"Tarefa com id {id} não encontrada"}), 404

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    try:
        with open(NOME_ARQUIVO, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo de dados não encontrado."}), 404
    dados_atualizados = [tarefa for tarefa in dados if tarefa.get('id') != id]
    if len(dados_atualizados) == len(dados):
        return jsonify({"erro": f"Tarefa com ID {id} não encontrada."}), 404
    with open(NOME_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(dados_atualizados, f, indent=4, ensure_ascii=False)
    return jsonify({"mensagem": f"Tarefa com ID {id} foi deletada com sucesso."}), 200