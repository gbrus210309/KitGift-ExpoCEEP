# KitGift — Relatório de Consolidação Final e Pitch: Etapa 5

**Curso:** Técnico em Desenvolvimento de Sistemas · **Turma:** 3M  
**Disciplina:** Programação Back-End · **Modalidade:** EXPOCEEP  
**Repositório:** https://github.com/gbrus210309/KitGift-ExpoCEEP

## 1. Identificação e divisão de papéis no pitch

- Gabriel Brustolin, nº 10 — demonstração do sistema e integração entre tela e API.
- Débora Dias, nº 5 — problema, solução e apresentação do banner.
- Hayat Rossi Azam, nº 13 — arquitetura Flask/SQLite e conclusão.

## 2. Comprovação de funcionamento do MVP

- A rota `POST /produtos` respondeu **HTTP 201 Created**.
- O produto **Kit Teste Pitch — Etapa 5**, ID 17, foi gravado na tabela `produtos` do SQLite.
- Os 9 testes automatizados foram aprovados e os arquivos JavaScript passaram na verificação de sintaxe.
- Evidência HTTP: `etapa5-evidencias/01-requisicao-http-201.png`.
- Evidência SQLite: `etapa5-evidencias/02-sqlite-produto-gravado.png`.

## 3. Autoavaliação e reflexão técnica

**a) Maior desafio técnico:** manter a comunicação entre o formulário em HTML/JavaScript, as rotas da API em Flask e o banco SQLite. Foi necessário padronizar o JSON enviado pelo fetch, validar os campos, retornar os códigos HTTP corretos e garantir que a vitrine e o painel administrativo exibissem os mesmos dados.

**b) Próxima funcionalidade:** implementar autenticação com senhas criptografadas, sessões e perfis de acesso para cliente e administrador. Depois, ligar esse cadastro ao carrinho, aos pedidos e ao histórico de compras, aproveitando as tabelas já existentes.

## 4. Avaliação da professora

Campo mantido em branco no PDF para preenchimento da professora.
