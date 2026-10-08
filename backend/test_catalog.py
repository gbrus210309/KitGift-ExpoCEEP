import sqlite3
import test_api
import unittest
from contextlib import closing


class CatalogTest(unittest.TestCase):
    setUp = test_api.APITest.setUp
    tearDown = test_api.APITest.tearDown
    create = test_api.APITest.create
    def test_catalog_follows_admin_changes(self):
        initial_catalog = self.client.get('/api/catalogo').json
        pid = self.create()
        product = next(item for item in self.client.get('/api/catalogo').json if item['id_produto'] == pid)
        self.assertEqual(product['categoria'], 'Presentes')
        self.client.put(f'/produtos/{pid}', json=dict(self.payload, preco=1234, estoque=0))
        product = next(item for item in self.client.get('/api/catalogo').json if item['id_produto'] == pid)
        self.assertEqual((product['preco'], product['estoque']), (1234, 0))
        self.client.put(f'/produtos/{pid}', json=dict(self.payload, ativo=0))
        self.assertEqual(self.client.get('/api/catalogo').json, initial_catalog)
        self.client.put(f'/produtos/{pid}', json=self.payload)
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('UPDATE categorias SET ativo=0')
        self.assertEqual(self.client.get('/api/catalogo').json, [])
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('UPDATE categorias SET ativo=1')
        self.client.delete(f'/produtos/{pid}')
        self.assertEqual(self.client.get('/api/catalogo').json, initial_catalog)

    def test_separate_pages(self):
        store = self.client.get('/')
        admin = self.client.get('/admin')
        catalog = self.client.get('/api/catalogo')
        try:
            self.assertIn(b'Descubra nossos kits', store.data)
            self.assertIn(b'product-form', admin.data)
            self.assertNotIn(b'product-form', store.data)
            self.assertEqual(catalog.headers['Cache-Control'], 'no-store')
        finally:
            store.close()
            admin.close()
            catalog.close()
