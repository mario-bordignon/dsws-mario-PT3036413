from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from .. import db
from ..models import User, Role
from ..email import notify_new_user
from . import main
from .forms import NameForm


# --- Relógio global (disponível em todos os templates) ---
@main.app_context_processor
def inject_time():
    return dict(current_time=datetime.utcnow())


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            # Role padrão para todo novo cadastro
            default_role = (Role.query.filter_by(name='Usuário').first()
                            or Role.query.filter_by(name='User').first())

            user = User(username=form.name.data, role=default_role)
            db.session.add(user)
            db.session.commit()

            # Destinatários fixos + o e-mail digitado no formulário
            resultados = notify_new_user(user, form.email.data)
            falhas = [dest for dest, ok in resultados.items() if not ok]

            if not falhas:
                flash('Usuário cadastrado e e-mail enviado com sucesso!', 'success')
            else:
                flash('Usuário cadastrado, mas não foi possível enviar e-mail para: '
                      + ', '.join(falhas) + '. No sandbox do Mailgun, o endereço '
                      'precisa estar autorizado.', 'warning')

            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))

    # Lista de usuários cadastrados (com a role de cada um)
    todos_os_usuarios = User.query.order_by(User.id).all()

    return render_template('index.html',
                           form=form,
                           nome_completo=session.get('name'),
                           known=session.get('known', False),
                           users=todos_os_usuarios)