import sqlite3
import test_api
import unittest
from contextlib import closing


class CatalogTest(unittest.TestCase):
    setUp = test_api.APITest.setUp
    tearDown = test_api.APITest.tearDown
    create = test_api.APITest.create
    def test_catalog_follows_admin_changes(self):
        self.assertEqual(self.client.get('/api/catalogo').json, [])
        pid = self.create()
        self.assertEqual(self.client.get('/api/catalogo').json[0]['categoria'], 'Presentes')
        self.client.put(f'/produtos/{pid}', json=dict(self.payload, preco=1234, estoque=0))
        product = self.client.get('/api/catalogo').json[0]
        self.assertEqual((product['preco'], product['estoque']), (1234, 0))
        self.client.put(f'/produtos/{pid}', json=dict(self.payload, ativo=0))
        self.assertEqual(self.client.get('/api/catalogo').json, [])
        self.client.put(f'/produtos/{pid}', json=self.payload)
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('UPDATE categorias SET ativo=0')
        self.assertEqual(self.client.get('/api/catalogo').json, [])
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('UPDATE categorias SET ativo=1')
        self.client.delete(f'/produtos/{pid}')
        self.assertEqual(self.client.get('/api/catalogo').json, [])

    def test_separate_pages(self):
        self.assertIn(b'Descubra nossos kits', self.client.get('/').data)
        self.assertIn(b'product-form', self.client.get('/admin').data)
        self.assertNotIn(b'product-form', self.client.get('/').data)
        self.assertEqual(self.client.get('/api/catalogo').headers['Cache-Control'], 'no-store')
