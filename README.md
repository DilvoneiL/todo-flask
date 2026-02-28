# To-Do Flask (Projeto Python Pro)

Projeto web simples desenvolvido com **Flask** para gerenciar tarefas (To-Do), com foco em uso de recursos da biblioteca (rotas, templates, flash messages e forms).

## Funcionalidades
- Criar tarefa (título, descrição e categoria)
- Listar tarefas
- Filtrar por status (todas / pendentes / concluídas)
- Buscar por título/descrição/categoria
- Marcar como concluída / reabrir
- Excluir tarefa
- Mensagens de feedback usando `flash()` do Flask

## Tecnologias
- Python 3
- Flask
- SQLite (biblioteca padrão do Python via `sqlite3`)

## Como executar (Windows / Linux / Mac)
1. Crie e ative um ambiente virtual:
   - Windows:
     ```bash
     python3 -m venv .venv
     .\.venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

2. Instale dependências:
   ```bash
   pip install -r requirements.txt
     ```

3. Rode o projeto:
    ```bash
    python3 app.py

```



Acesse: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Estrutura

```text
todo-flask/
  app.py
  requirements.txt
  README.md
  templates/
  static/

```

## Observações

O banco `todo.db` é criado automaticamente ao iniciar o projeto.

