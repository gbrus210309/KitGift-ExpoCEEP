"""Testes de integração com SQLite temporário, sem tocar no banco do grupo."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from app import create_app


class APITest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'teste.db'
        self.app = create_app(self.path)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.category = self.client.post('/categorias', json={'nome': 'Presentes'}).json['id_categoria']
        self.payload = {'nome': 'Kit carinho', 'id_categoria': self.category, 'preco': 5990, 'estoque': 5}

    def tearDown(self):
        self.temp.cleanup()

    def create(self):
        response = self.client.post('/produtos', json=self.payload)
        self.assertEqual(response.status_code, 201)
        return response.json['id_produto']

    def test_crud_and_persistence(self):
        pid = self.create()
        other = self.create()
        restarted = create_app(self.path).test_client()
        self.assertEqual(len(restarted.get('/produtos').json), 2)
        self.assertEqual(restarted.get(f'/produtos/{pid}').json['preco'], 5990)
        changed = dict(self.payload, nome='Kit carinho premium', preco=7990, estoque=3)
        self.assertEqual(self.client.put(f'/produtos/{pid}', json=changed).status_code, 200)
        self.assertEqual(restarted.get(f'/produtos/{pid}').json['nome'], changed['nome'])
        self.assertEqual(restarted.get(f'/produtos/{other}').json['nome'], self.payload['nome'])
        self.assertEqual(self.client.delete(f'/produtos/{pid}').status_code, 200)
        self.assertEqual(self.client.delete(f'/produtos/{pid}').status_code, 404)
        self.assertEqual(restarted.get(f'/produtos/{pid}').status_code, 404)
        self.assertEqual(restarted.get(f'/produtos/{other}').status_code, 200)
        self.assertEqual(self.client.put(f'/produtos/{pid}', json=changed).status_code, 404)

    def test_invalid_bodies(self):
        for payload in (None, [], 'texto', 2, {}, {'nome': '   '}):
            with self.subTest(payload=payload):
                response = self.client.post('/produtos', data=__import__('json').dumps(payload), content_type='application/json')
                self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.post('/produtos', data='{', content_type='application/json').status_code, 400)
        self.assertEqual(self.client.post('/produtos', data='nome=Kit').status_code, 415)

    def test_invalid_fields_do_not_change_records(self):
        pid = self.create()
        for field, value in [('nome', 1), ('nome', ''), ('preco', -1), ('preco', 1.5),
                             ('preco', True), ('preco', 10**30), ('estoque', -1),
                             ('id_categoria', 9999), ('id_categoria', True),
                             ('ativo', 2), ('descricao', []), ('imagem', {}), ('extra', 'x')]:
            with self.subTest(field=field, value=value):
                payload = dict(self.payload, **{field: value})
                self.assertEqual(self.client.post('/produtos', json=payload).status_code, 400)
                self.assertEqual(self.client.put(f'/produtos/{pid}', json=payload).status_code, 400)
        self.assertEqual(self.client.get(f'/produtos/{pid}').json['preco'], 5990)
        self.assertEqual(len(self.client.get('/produtos').json), 1)

    def test_related_product_cannot_be_deleted(self):
        pid = self.create()
        with sqlite3.connect(self.path) as conn:
            conn.execute("INSERT INTO usuarios (nome,email,senha) VALUES ('Teste','teste@example.invalid','hash-ficticio')")
            conn.execute('INSERT INTO carrinhos (id_usuario) VALUES (1)')
            conn.execute('INSERT INTO itens_carrinho (id_carrinho,id_produto,quantidade,preco_unitario) VALUES (1,?,1,5990)', (pid,))
        conn.close()
        self.assertEqual(self.client.delete(f'/produtos/{pid}').status_code, 409)
        self.assertEqual(self.client.get(f'/produtos/{pid}').status_code, 200)

    def test_categories_and_sql_parameters(self):
        self.assertEqual(self.client.post('/categorias', json={'nome': 'Presentes'}).status_code, 409)
        self.assertEqual(self.client.post('/categorias', json={'nome': ''}).status_code, 400)
        self.assertEqual(self.client.get('/categorias').status_code, 200)
        self.payload['nome'] = "Kit'); DROP TABLE produtos; --"
        pid = self.create()
        self.assertEqual(self.client.get(f'/produtos/{pid}').json['nome'], self.payload['nome'])
        self.assertEqual(self.client.get('/produtos').status_code, 200)

    def test_unknown_route_and_method_are_json(self):
        for response, status in [(self.client.get('/inexistente'), 404), (self.client.patch('/produtos/1'), 405)]:
            self.assertEqual(response.status_code, status)
            self.assertIn('erro', response.json)

    def test_web_page_assets_and_database_are_isolated(self):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        self.assertIn(b'product-form', response.data)
        response.close()
        for path in ('/assets/main.js', '/assets/style.css'):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            response.close()
        self.assertEqual(self.client.get('/api/status').status_code, 200)
        self.assertEqual(self.client.get('/assets/../bd/banco.db').status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
