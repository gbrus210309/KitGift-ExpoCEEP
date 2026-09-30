"""KitGift: interface da Etapa 3 e API local com CRUD de produtos."""
import os
import sqlite3
from contextlib import closing

from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

try:
    from .database import DB_PATH, get_db_connection, initialize_database
except ImportError:
    from database import DB_PATH, get_db_connection, initialize_database


def create_app(database_path=None):
    app = Flask(__name__)
    app.config['DATABASE'] = str(database_path or os.environ.get('KITGIFT_DB_PATH') or DB_PATH)
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
    CORS(app)
    initialize_database(app.config['DATABASE'])

    def connection():
        return get_db_connection(app.config['DATABASE'])

    def body():
        if not request.is_json:
            return None, (jsonify(erro='Envie Content-Type: application/json.'), 415)
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return None, (jsonify(erro='O corpo deve ser um objeto JSON válido.'), 400)
        return data, None

    def validate_product(data):
        allowed = {'nome', 'id_categoria', 'preco', 'estoque', 'descricao', 'imagem', 'ativo'}
        if set(data) - allowed:
            return None, 'Há campos desconhecidos no JSON.'
        if not isinstance(data.get('nome'), str) or not data['nome'].strip():
            return None, 'O campo nome é obrigatório e deve ser um texto não vazio.'
        for field in ('id_categoria', 'preco', 'estoque'):
            value = data.get(field)
            minimum = 1 if field == 'id_categoria' else 0
            if type(value) is not int or not minimum <= value <= 2147483647:
                return None, f'{field} deve ser inteiro entre {minimum} e 2147483647.'
        for field in ('descricao', 'imagem'):
            if data.get(field) is not None and not isinstance(data[field], str):
                return None, f'{field} deve ser texto ou null.'
        active = data.get('ativo', 1)
        if type(active) is not int or active not in (0, 1):
            return None, 'ativo deve ser 0 ou 1.'
        return (data['id_categoria'], data['nome'].strip(), data.get('descricao'),
                data['preco'], data['estoque'], data.get('imagem'), active), None

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(erro=error.description), error.code

    @app.errorhandler(sqlite3.IntegrityError)
    def integrity_error(error):
        return jsonify(erro='Operação em conflito com registros existentes ou relacionados.'), 409

    @app.errorhandler(sqlite3.OperationalError)
    def database_error(error):
        app.logger.exception('Falha de acesso ao SQLite')
        return jsonify(erro='Banco temporariamente indisponível.'), 503

    @app.get('/')
    def index():
        return send_from_directory(Path(__file__).resolve().parents[1] / 'frontend', 'loja.html')

    @app.get('/admin')
    def admin():
        return send_from_directory(Path(__file__).resolve().parents[1] / 'frontend', 'index.html')

    @app.get('/api/catalogo')
    def catalog():
        with closing(connection()) as conn:
            rows = conn.execute('''SELECT p.*, c.nome AS categoria FROM produtos p
                JOIN categorias c ON c.id_categoria = p.id_categoria
                WHERE p.ativo = 1 AND c.ativo = 1 ORDER BY p.id_produto DESC''').fetchall()
        response = jsonify([dict(row) for row in rows])
        response.headers['Cache-Control'] = 'no-store'
        return response

    @app.get('/assets/<path:filename>')
    def assets(filename):
        return send_from_directory(Path(__file__).resolve().parents[1] / 'frontend', filename)

    @app.get('/api/status')
    def status_api():
        return jsonify(status='sucesso', mensagem='API do KitGift - Etapa 3: interface e SQLite.'), 200

    @app.get('/categorias')
    def list_categories():
        with closing(connection()) as conn:
            rows = conn.execute('SELECT * FROM categorias ORDER BY id_categoria').fetchall()
        return jsonify([dict(row) for row in rows]), 200

    @app.post('/categorias')
    def create_category():
        data, error = body()
        if error:
            return error
        if set(data) - {'nome', 'descricao'}:
            return jsonify(erro='Use apenas nome e descricao.'), 400
        if not isinstance(data.get('nome'), str) or not data['nome'].strip():
            return jsonify(erro='nome é obrigatório e deve ser texto não vazio.'), 400
        if data.get('descricao') is not None and not isinstance(data['descricao'], str):
            return jsonify(erro='descricao deve ser texto ou null.'), 400
        with closing(connection()) as conn, conn:
            cursor = conn.execute('INSERT INTO categorias (nome, descricao) VALUES (?, ?)',
                                  (data['nome'].strip(), data.get('descricao')))
            category_id = cursor.lastrowid
        return jsonify(mensagem='Categoria cadastrada com sucesso!', id_categoria=category_id), 201

    @app.get('/produtos')
    def list_products():
        with closing(connection()) as conn:
            rows = conn.execute('SELECT * FROM produtos ORDER BY id_produto').fetchall()
        return jsonify([dict(row) for row in rows]), 200

    @app.get('/produtos/<int:product_id>')
    def get_product(product_id):
        with closing(connection()) as conn:
            row = conn.execute('SELECT * FROM produtos WHERE id_produto = ?', (product_id,)).fetchone()
        if row is None:
            return jsonify(erro='Produto não encontrado.'), 404
        return jsonify(dict(row)), 200

    @app.post('/produtos')
    def create_product():
        data, error = body()
        if error:
            return error
        values, error = validate_product(data)
        if error:
            return jsonify(erro=error), 400
        with closing(connection()) as conn, conn:
            if conn.execute('SELECT 1 FROM categorias WHERE id_categoria = ?', (values[0],)).fetchone() is None:
                return jsonify(erro='Categoria não encontrada.'), 400
            cursor = conn.execute('''INSERT INTO produtos
                (id_categoria, nome, descricao, preco, estoque, imagem, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
            product_id = cursor.lastrowid
        return jsonify(mensagem='Produto cadastrado com sucesso!', id_produto=product_id), 201

    @app.put('/produtos/<int:product_id>')
    def update_product(product_id):
        data, error = body()
        if error:
            return error
        values, error = validate_product(data)
        if error:
            return jsonify(erro=error), 400
        with closing(connection()) as conn, conn:
            if conn.execute('SELECT 1 FROM produtos WHERE id_produto = ?', (product_id,)).fetchone() is None:
                return jsonify(erro='Produto não encontrado.'), 404
            if conn.execute('SELECT 1 FROM categorias WHERE id_categoria = ?', (values[0],)).fetchone() is None:
                return jsonify(erro='Categoria não encontrada.'), 400
            conn.execute('''UPDATE produtos SET id_categoria = ?, nome = ?, descricao = ?,
                preco = ?, estoque = ?, imagem = ?, ativo = ? WHERE id_produto = ?''', values + (product_id,))
        return jsonify(mensagem='Produto atualizado com sucesso!'), 200

    @app.delete('/produtos/<int:product_id>')
    def delete_product(product_id):
        with closing(connection()) as conn, conn:
            cursor = conn.execute('DELETE FROM produtos WHERE id_produto = ?', (product_id,))
            if cursor.rowcount == 0:
                return jsonify(erro='Produto não encontrado.'), 404
        return jsonify(mensagem='Produto removido com sucesso!'), 200

    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=5000, debug=False)
