# Desenvolvimento Web com Flask

Repositório referente às aulas de DSWS
Aluno: Mario Antonio Bordignon
Prontuário: PT3036413

## Estrutura do projeto

```
├── app/
│   ├── __init__.py        # create_app() (application factory) e extensões
│   ├── models.py          # Role, User, EmailEnviado
│   ├── email.py           # envio de e-mail via Mailgun + registro no banco
│   ├── main/              # blueprint "main"
│   │   ├── __init__.py
│   │   ├── errors.py      # páginas 404 e 500
│   │   ├── forms.py       # NameForm
│   │   └── views.py       # rotas: / e /emails
│   ├── static/            # favicon
│   └── templates/         # base, index, emails, 404, 500
├── migrations/
├── tests/
├── config.py              # configurações (development / testing / production)
├── flasky.py              # ponto de entrada (FLASK_APP)
├── requirements.txt
└── .env.example
```

## 1. Preparando o ambiente

```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Variáveis de ambiente

Copie `.env.example` para `.env` e preencha com as chaves do Mailgun.
O `.env` não vai para o GitHub.

## 3. Criando o banco de dados

```powershell
flask shell
```

```python
db.create_all()
db.session.add(Role(name='Usuário'))
db.session.commit()
exit()
```

Quando os modelos mudarem, use as migrações:

```powershell
flask db migrate -m "descrição da mudança"
flask db upgrade
```

## 4. Iniciando localmente

```powershell
flask run --debug
```

Acesse: http://127.0.0.1:5000

## 5. Testes

```powershell
flask test
```

## 6. Produção (PythonAnywhere)

No `.env` do servidor, defina `FLASK_CONFIG=production` (usa o banco `data.sqlite`).
No arquivo WSGI da web app, importe a aplicação assim:

```python
from flasky import app as application
```
