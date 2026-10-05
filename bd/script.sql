-- KitGift - Etapa 1. Valores monetários em centavos (INTEGER).
-- Execute em um banco novo. Ative foreign_keys em cada conexão SQLite.
PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL, -- Reservado para hash de senha; não armazenar texto puro.
    telefone TEXT,
    cpf TEXT UNIQUE,
    data_nascimento TEXT,
    tipo TEXT NOT NULL DEFAULT 'cliente' CHECK (tipo IN ('cliente', 'adm')),
    data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enderecos (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
    logradouro TEXT NOT NULL,
    numero TEXT NOT NULL,
    complemento TEXT,
    bairro TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    cep TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'entrega' CHECK (tipo IN ('entrega', 'cobranca'))
);

CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER NOT NULL REFERENCES categorias(id_categoria),
    nome TEXT NOT NULL,
    descricao TEXT,
    preco INTEGER NOT NULL CHECK (typeof(preco) = 'integer' AND preco >= 0),
    estoque INTEGER NOT NULL DEFAULT 0 CHECK (typeof(estoque) = 'integer' AND estoque >= 0),
    imagem TEXT,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE carrinhos (
    id_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL UNIQUE REFERENCES usuarios(id),
    data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total INTEGER NOT NULL DEFAULT 0 CHECK (typeof(total) = 'integer' AND total >= 0)
);

CREATE TABLE itens_carrinho (
    id_item_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
    id_carrinho INTEGER NOT NULL REFERENCES carrinhos(id_carrinho) ON DELETE CASCADE,
    id_produto INTEGER NOT NULL REFERENCES produtos(id_produto),
    quantidade INTEGER NOT NULL CHECK (typeof(quantidade) = 'integer' AND quantidade > 0),
    preco_unitario INTEGER NOT NULL CHECK (typeof(preco_unitario) = 'integer' AND preco_unitario >= 0),
    subtotal INTEGER GENERATED ALWAYS AS (quantidade * preco_unitario) STORED,
    UNIQUE (id_carrinho, id_produto)
);

CREATE TABLE pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
    data_pedido TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'pago', 'preparando', 'enviado', 'entregue', 'cancelado')),
    valor_total INTEGER NOT NULL DEFAULT 0 CHECK (typeof(valor_total) = 'integer' AND valor_total >= 0),
    endereco_entrega TEXT NOT NULL, -- Cópia do endereço no momento da compra.
    data_entrega TEXT
);

CREATE TABLE itens_pedido (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL REFERENCES pedidos(id_pedido),
    id_produto INTEGER NOT NULL REFERENCES produtos(id_produto),
    quantidade INTEGER NOT NULL CHECK (typeof(quantidade) = 'integer' AND quantidade > 0),
    preco_unitario INTEGER NOT NULL CHECK (typeof(preco_unitario) = 'integer' AND preco_unitario >= 0),
    subtotal INTEGER GENERATED ALWAYS AS (quantidade * preco_unitario) STORED,
    UNIQUE (id_pedido, id_produto)
);

CREATE TABLE pagamentos (
    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL REFERENCES pedidos(id_pedido),
    metodo_pagamento TEXT NOT NULL CHECK (metodo_pagamento IN ('pix', 'cartao', 'boleto')),
    status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'aprovado', 'recusado', 'estornado')),
    valor_pago INTEGER NOT NULL CHECK (typeof(valor_pago) = 'integer' AND valor_pago >= 0),
    data_pagamento TEXT,
    transacao_id TEXT UNIQUE
);

-- Catálogo inicial criado pelo painel administrativo.
INSERT INTO categorias (nome, descricao) VALUES
    ('Escolar', 'Kits para estudo, organização e volta às aulas.'),
    ('Datas especiais', 'Presentes para celebrar pessoas e momentos importantes.'),
    ('Lazer', 'Kits para aproveitar momentos de descanso e diversão.');

INSERT INTO produtos (id_categoria, nome, descricao, preco, estoque, imagem) VALUES
    ((SELECT id_categoria FROM categorias WHERE nome = 'Escolar'),
     'Kit Volta às Aulas',
     'Cadernos, estojo e materiais essenciais reunidos para começar o ano letivo com praticidade e organização.',
     8990, 15, '/assets/images/kit-volta-as-aulas.png'),
    ((SELECT id_categoria FROM categorias WHERE nome = 'Datas especiais'),
     'Kit Dia das Mães — Carinho e Relaxamento',
     'Caneca, vela aromática, itens de autocuidado, flores e chocolates para transformar carinho em um momento especial.',
     12990, 10, '/assets/images/kit-dia-das-maes.png'),
    ((SELECT id_categoria FROM categorias WHERE nome = 'Datas especiais'),
     'Kit Dia dos Pais — Café e Companhia',
     'Café, caneca, caderno, caneta e chocolates em uma seleção elegante para celebrar quem está sempre presente.',
     11990, 8, '/assets/images/kit-dia-dos-pais.png'),
    ((SELECT id_categoria FROM categorias WHERE nome = 'Datas especiais'),
     'Kit Aniversário — Celebração',
     'Cupcake, bebida, chocolates e itens de festa reunidos para deixar qualquer aniversário mais alegre.',
     9990, 12, '/assets/images/kit-aniversario.png'),
    ((SELECT id_categoria FROM categorias WHERE nome = 'Lazer'),
     'Kit Sessão Cinema',
     'Pipoca, chocolates, bebidas e uma manta aconchegante para curtir uma sessão de cinema sem sair de casa.',
     7490, 18, '/assets/images/kit-sessao-cinema.png');

COMMIT;
