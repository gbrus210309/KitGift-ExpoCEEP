# KitGift

Projeto de e-commerce de kits de produtos complementares - EXPOCEEP, turma 3M. Protótipo de gestão de kits com HTML/CSS/JavaScript, Python/Flask e SQLite.

Repositório oficial: https://github.com/gbrus210309/KitGift-ExpoCEEP

Etapa 4 - EXPOCEEP: [relatório técnico](docs/Relatorio-Etapa4-KitGift.pdf) e [banner recebido da equipe](docs/Banner-KitGift-ExpoCEEP.pdf). Consulte as pendências no [registro da etapa](docs/etapa4-progresso.md).

## Interface da Etapa 3

Inicie o servidor pelos comandos abaixo. A vitrine fica em http://127.0.0.1:5000/ e a gestão descrita nesta seção em http://127.0.0.1:5000/admin.
A página contém cadastro de categorias, formulário de kits, listagem dinâmica via fetch e exclusão com confirmação. A atualização de produtos (PUT) está disponível na API, mas ainda não tem formulário na interface.
Os arquivos visuais ficam em `frontend/index.html`, `frontend/style.css` e `frontend/main.js`.
A rota de diagnóstico JSON foi movida de `/` para `/api/status`.
Não abra o HTML com duplo clique: a interface deve ser servida pelo Flask.
Veja [o registro da Etapa 3](docs/etapa3-progresso.md), [o relatório em PDF](docs/Relatorio-Etapa3-KitGift.pdf) e [as capturas de funcionamento](docs/etapa3-evidencias/).

## Equipe

- Gabriel Brustolin - nº 10
- Débora Dias - nº 5
- Hayat Rossi Azam - nº 13

## Entrega atual

API Python/Flask conectada ao SQLite, com CRUD completo de produtos e cadastro/listagem de categorias. A interface da Etapa 3 foi validada no navegador: cadastro via fetch, listagem dinâmica, mensagens de erro e persistência após reiniciar o servidor. O relatório e as quatro capturas estão em docs/. O banco mantém as nove tabelas da Etapa 1. Login, checkout e pagamento real não fazem parte desta entrega. Esta API de laboratório, sem autenticação, deve ser executada apenas localmente.

## Estrutura

```text
KitGift/
├── .gitignore
├── README.md
├── bd/
│   ├── script.sql
│   └── init_db.py
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── test_api.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── main.js
└── docs/
    ├── Relatorio-Etapa3-KitGift.pdf
    ├── etapa3-evidencias/
    ├── etapa3-progresso.md
    ├── modelagem.md
    ├── etapa2.md
    ├── KitGift-Etapa2.postman_collection.json
    └── evidencias-http.json
```

## Executar no Windows

Requer Python 3.10 ou superior e SQLite 3.31 ou superior. Abra a pasta raiz no VS Code. No terminal:

```powershell
python -m venv backend/venv
.\backend\venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\backend\venv\Scripts\python.exe backend/app.py
```

Acesse http://localhost:5000/api/status para receber:

```json
{"status":"sucesso","mensagem":"API do KitGift - Etapa 3: interface e SQLite."}
```

A API cria `bd/banco.db` automaticamente quando o banco está vazio. Ao reiniciar, os registros são preservados. Bancos da Etapa 1 com o esquema completo são reutilizados. Um banco antigo com apenas usuários será recusado: preserve uma cópia e utilize um arquivo novo, pois não há migração automática. `bd/init_db.py` continua disponível para inicialização manual de bancos novos. O caminho é calculado a partir do arquivo Python, independente da pasta do terminal.

## Rotas da aplicação

URL base: `http://127.0.0.1:5000`. As rotas de dados retornam JSON. POST e PUT exigem o cabeçalho `Content-Type: application/json`.

| Método | Rota | Resultado |
|---|---|---|
| GET | `/` | Interface HTML, 200 |
| GET | `/assets/<arquivo>` | CSS/JavaScript da interface, 200 ou 404 |
| GET | `/api/status` | Diagnóstico JSON, 200 |
| POST | `/categorias` | Cria categoria, 201 |
| GET | `/categorias` | Lista categorias, 200 |
| POST | `/produtos` | Cria produto, 201 |
| GET | `/produtos` | Lista produtos, 200 |
| GET | `/produtos/<id>` | Consulta produto, 200 ou 404 |
| PUT | `/produtos/<id>` | Atualiza produto, 200 ou 404 |
| DELETE | `/produtos/<id>` | Exclui produto, 200 ou 404; 409 se vinculado |

### Exemplos de requisições e respostas

Os IDs abaixo são ilustrativos. Use o `id_categoria` e o `id_produto` retornados pelo seu banco, sem presumir que serão 1. Em GET e DELETE não é necessário enviar corpo.

**POST /categorias** - criar uma categoria antes de cadastrar kits:

```json
{"nome":"Presentes","descricao":"Kits para diferentes ocasiões"}
```

Resposta 201:

```json
{"id_categoria":1,"mensagem":"Categoria cadastrada com sucesso!"}
```

**GET /categorias** - resposta 200; retorna `[]` se não houver registros:

```json
[{"id_categoria":1,"nome":"Presentes","descricao":"Kits para diferentes ocasiões","ativo":1}]
```

**POST /produtos** - cadastrar um kit (5990 centavos = R$ 59,90):

```json
{"nome":"Kit carinho","id_categoria":1,"preco":5990,"estoque":5,"descricao":"Caneca e chocolates"}
```

Resposta 201:

```json
{"id_produto":1,"mensagem":"Produto cadastrado com sucesso!"}
```

**GET /produtos** - resposta 200; retorna `[]` se não houver kits:

```json
[{"id_produto":1,"id_categoria":1,"nome":"Kit carinho","descricao":"Caneca e chocolates","preco":5990,"estoque":5,"imagem":null,"ativo":1}]
```

**GET /produtos/1** - resposta 200 para um produto existente:

```json
{"id_produto":1,"id_categoria":1,"nome":"Kit carinho","descricao":"Caneca e chocolates","preco":5990,"estoque":5,"imagem":null,"ativo":1}
```

**PUT /produtos/1** - atualizar um kit. Envie todos os campos obrigatórios; não é uma atualização parcial. Omitir `descricao` ou `imagem` redefine esses campos para `null`; omitir `ativo` redefine para 1.

```json
{"nome":"Kit carinho premium","id_categoria":1,"preco":7990,"estoque":3,"descricao":"Caneca e chocolates especiais","imagem":null,"ativo":1}
```

Resposta 200:

```json
{"mensagem":"Produto atualizado com sucesso!"}
```

**DELETE /produtos/1** - exclui definitivamente um kit sem vínculos. Resposta 200:

```json
{"mensagem":"Produto removido com sucesso!"}
```

### Validações e erros

- Categoria: `nome` é obrigatório e não pode ser vazio; `descricao` é texto ou `null`. Nomes repetidos geram conflito. Outros campos são rejeitados.
- Produto: `nome`, `id_categoria`, `preco` e `estoque` são obrigatórios. Nome deve ser texto não vazio. Categoria deve existir.
- `id_categoria`: inteiro entre 1 e 2147483647. `preco` e `estoque`: inteiros entre 0 e 2147483647. Valores booleanos não são aceitos como inteiros.
- Campos opcionais: `descricao` e `imagem` aceitam texto ou `null`; `ativo` aceita o inteiro 0 ou 1. A interface não exibe a imagem do produto nesta versão.
- Campos desconhecidos, JSON inválido ou valores inválidos: 400. Tipo de conteúdo diferente de JSON em POST/PUT: 415.
- Produto ou rota inexistente: 404. Método não permitido: 405. Corpo acima de 1 MiB: 413. Falha operacional no SQLite: 503.
- Categoria duplicada ou exclusão de produto vinculado a carrinho/pedido: 409. As chaves estrangeiras preservam os registros relacionados.

Exemplos de respostas de erro:

```json
{"erro":"Categoria não encontrada."}
```

```json
{"erro":"Produto não encontrado."}
```

```json
{"erro":"Operação em conflito com registros existentes ou relacionados."}
```

## Testes e demonstração

Consulte [payloads, validações e roteiro de evidências](docs/etapa2.md). Importe [a coleção Postman](docs/KitGift-Etapa2.postman_collection.json) e execute na ordem. Ela armazena os IDs retornados e confere os status HTTP. Todos os dados de demonstração são fictícios.

Na interface: adicione uma categoria, cadastre um kit, confira a listagem e recarregue a página para verificar a persistência. Para demonstrar exclusão, crie um kit fictício descartável e use “Excluir kit”, confirmando seu nome. Para encerrar o servidor, pressione Ctrl+C no terminal. Em próximos usos, execute apenas o comando que inicia `backend/app.py`; não é necessário recriar o ambiente virtual.

Se `python` não for reconhecido, confira se o Python está instalado e tente `py` no comando de criação do ambiente. Se a página não abrir, mantenha o servidor ligado e confira o endereço mostrado no terminal. Não tente abrir o site pelo arquivo HTML nem trate o link do GitHub como hospedagem da aplicação.

Para executar os sete testes de integração com um banco temporário:

```powershell
.\backend\venv\Scripts\python.exe -m unittest discover -s backend -p test_api.py -v
```

Os testes cobrem CRUD, persistência após recriar a aplicação, isolamento de registros, JSON inválido, tipos e valores inválidos, categoria inexistente, SQL parametrizado e bloqueio de exclusão de produtos relacionados. `docs/evidencias-http.json` contém respostas de 12 requisições HTTP reais executadas com Python; esse registro não substitui os prints no Thunder Client/Postman exigidos pelo relatório.

## Banco de dados

Veja [modelagem e relacionamentos](docs/modelagem.md). Preços e totais são inteiros em centavos: R$ 25,90 = 2590. Subtotais são calculados pelo SQLite. Os totais de carrinhos e pedidos deverão ser atualizados pela futura lógica de compra, na mesma transação dos itens. Nenhum pagamento real é processado e nenhum dado de cartão deve ser armazenado.

Foi preservada a chave `usuarios.id` do código original. Os endereços ficam em tabela própria para evitar duplicidade no cadastro. Cada pedido guarda uma cópia textual do endereço de entrega. A coluna `senha` deverá receber apenas hashes quando o cadastro for implementado. Cada conexão futura deve executar `PRAGMA foreign_keys = ON`.

## Evidências para o relatório

O relatório da Etapa 2 deve incluir integrantes, turma, link público e quatro capturas do Thunder Client/Postman: POST com 201, GET com 200, PUT com 200 e DELETE com 200. Veja o roteiro em `docs/etapa2.md`. Não reutilize os prints da Etapa 1 como comprovação do CRUD.

O `.gitignore` exclui ambientes virtuais, bancos locais, caches, configurações locais e `.env`. Somente código e documentação devem ser versionados.


## Vitrine do cliente

Com o servidor iniciado, abra http://127.0.0.1:5000/ para a vitrine ou http://127.0.0.1:5000/admin para cadastrar e excluir kits. Ambos usam o mesmo SQLite. A vitrine consulta GET /api/catalogo, que retorna somente produtos ativos de categorias ativas, incluindo o nome da categoria. Kits sem estoque aparecem como esgotados.

A vitrine permite buscar por nome/descrição/categoria, filtrar, ordenar por preço e abrir detalhes. Recarrega os dados a cada 15 segundos enquanto visível, ao voltar para a aba e pelo botão Atualizar catálogo. O cadastro aceita URL opcional de imagem. Imagens ausentes ou indisponíveis usam uma apresentação textual da categoria. Não há produtos fictícios inseridos automaticamente.

Arquivos da vitrine: frontend/loja.html, frontend/loja.css e frontend/loja.js. A tela de gestão permanece em frontend/index.html. Compras, carrinho e pagamentos não estão implementados. A separação /admin não é autenticação: a API de escrita segue sem login. Executar localmente para a demonstração; antes de publicar o sistema na internet, implementar autenticação e autorização.
