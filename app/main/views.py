from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import User, Role, EmailEnviado
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

            # Fixos sempre; a conta da caixa só se estiver marcada
            destinatarios = list(current_app.config['FLASKY_DESTINATARIOS_FIXOS'])
            caixa = current_app.config['FLASKY_CAIXA']
            if form.enviar_caixa.data and caixa and caixa not in destinatarios:
                destinatarios.append(caixa)

            if notify_new_user(user, destinatarios):
                flash('Usuário cadastrado e e-mail enviado com sucesso!', 'success')
            else:
                flash('Usuário cadastrado, mas ocorreu um erro ao enviar o e-mail.', 'warning')

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


@main.route('/emails')
def emails_enviados():
    todos_os_emails = EmailEnviado.query.order_by(EmailEnviado.data_hora.desc()).all()
    return render_template('emails.html', emails=todos_os_emails)
