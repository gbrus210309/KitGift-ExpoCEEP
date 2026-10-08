# KitGift — Roteiro do Pitch da Etapa 5

**Modalidade:** EXPOCEEP · **Duração planejada:** 4min15s  
**Repositório:** https://github.com/gbrus210309/KitGift-ExpoCEEP

## Divisão do tempo

- **0:00–0:55 — Débora:** problema, exemplos de uso e proposta.
- **0:55–2:30 — Gabriel:** vitrine, painel administrativo e cadastro ao vivo.
- **2:30–3:45 — Hayat:** JavaScript, Flask, SQLite e segurança básica.
- **3:45–4:15 — Hayat:** próximos passos e conclusão.

## Falas

### Débora — problema e solução

Boa tarde. Nosso projeto se chama KitGift. A ideia surgiu para ajudar pessoas que querem comprar produtos que combinam, mas não desejam procurar cada item separadamente. Um exemplo é um kit de volta às aulas com os materiais essenciais, ou uma cesta pronta para o Dia dos Pais ou Dia das Mães. Nossa solução reúne essas opções em uma vitrine simples. O cliente consegue pesquisar, filtrar por categoria, ordenar por preço e abrir os detalhes de cada kit. Assim, a escolha fica mais rápida e organizada.

### Gabriel — demonstração ao vivo

Esta é a vitrine que o cliente acessa. Os kits exibidos aqui vêm do banco de dados. Podemos buscar um kit, filtrar a categoria, ordenar os resultados e abrir os detalhes. Agora vou acessar o painel administrativo. Nele escolhemos uma categoria, informamos nome, preço, estoque e descrição. Ao cadastrar, o JavaScript envia esses dados para a rota POST da API. A resposta de sucesso é HTTP 201. Quando atualizamos a vitrine, o novo kit aparece porque as duas telas consultam o mesmo servidor e o mesmo banco SQLite. O painel também permite excluir um kit quando ele não possui registros relacionados.

### Hayat — arquitetura e conclusão

Por trás da interface usamos HTML e CSS para a estrutura e o visual, e JavaScript com fetch para enviar e buscar dados em JSON. O Back-End foi feito em Python com Flask. A rota POST /produtos valida os campos e executa um INSERT parametrizado no SQLite. Os sinais de interrogação da consulta separam os valores do comando SQL e ajudam a evitar SQL Injection. Para montar a vitrine, a rota GET /api/catalogo retorna somente produtos e categorias ativos. Se o servidor estiver desligado, a requisição falha e a interface exibe uma mensagem de erro. Como próximos passos, implementaríamos autenticação com senha criptografada e perfis de cliente e administrador, seguida de carrinho e pedidos. O KitGift demonstra que a interface, a API e o banco já trabalham de forma integrada. Obrigado.

## Cadastro da demonstração

- Nome: Kit Demonstração EXPOCEEP
- Categoria: uma categoria existente
- Preço: R$ 64,90
- Estoque: 4
- Descrição: Caneca, chocolate e cartão para presentear.

## Código para mostrar

- `frontend/main.js`: cadastro e fetch para `POST /produtos`.
- `backend/app.py`: rota POST, validação e INSERT parametrizado.
- `backend/app.py`: rota `GET /api/catalogo`.
- `backend/database.py`: conexão SQLite e chaves estrangeiras.
- `bd/script.sql`: tabelas e relacionamentos.

## Perguntas e respostas rápidas

1. **Onde os dados são salvos?** O JavaScript envia JSON para o Flask, que grava na tabela produtos do SQLite.
2. **Como o painel atualiza a vitrine?** As duas telas usam o mesmo Back-End e o mesmo banco.
3. **E se o servidor estiver desligado?** O fetch falha e a interface mostra uma mensagem de erro.
4. **Como evitam SQL Injection?** Com consultas parametrizadas e valores separados do comando SQL.
5. **Por que SQLite?** É leve, local e suficiente para o protótipo.
6. **O que são 200 e 201?** 200 indica sucesso; 201 indica criação de um registro.
7. **Por que preço em centavos?** Para evitar erros de arredondamento monetário.
8. **Já vende pelo site?** Ainda não; carrinho, autenticação e pagamento são próximos passos.
9. **Para que servem chaves estrangeiras?** Para preservar a consistência entre as tabelas.
10. **Próxima função?** Autenticação com hash de senha, sessões e permissões.

## Comando para iniciar

```powershell
.\backend\venv\Scripts\python.exe backend/app.py
```

Vitrine: http://127.0.0.1:5000/  
Painel: http://127.0.0.1:5000/admin

## Plano de recuperação

- Site não abre: conferir o terminal e reiniciar o Flask.
- Porta ocupada: usar `Ctrl+C` no terminal antigo e iniciar uma única vez.
- Cadastro falha: conferir categoria, preço e estoque.
- Vitrine não atualiza: usar o botão Atualizar catálogo ou `Ctrl+F5`.
- Falha inesperada: mostrar as evidências HTTP 201 e SQLite presentes no relatório.
