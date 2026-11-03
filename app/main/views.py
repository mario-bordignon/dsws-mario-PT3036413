from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from .. import db
from ..models import User, Role
from ..email import notify_new_user
from . import main
from .forms import NameForm, EditUserForm, DeleteForm


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
                           users=todos_os_usuarios,
                           edit_form=EditUserForm(),
                           delete_form=DeleteForm())


@main.route('/usuarios/<int:user_id>/editar', methods=['POST'])
def editar_usuario(user_id):
    user = db.get_or_404(User, user_id)
    form = EditUserForm()
    if not form.validate_on_submit():
        for erros in form.errors.values():
            for erro in erros:
                flash(erro, 'warning')
        return redirect(url_for('.index'))

    novo_nome = form.name.data.strip()
    outro = User.query.filter(User.username == novo_nome,
                              User.id != user.id).first()
    if outro:
        flash('Já existe um usuário com esse nome.', 'warning')
        return redirect(url_for('.index'))

    user.username = novo_nome
    db.session.commit()
    flash('Nome do usuário atualizado com sucesso.', 'success')
    return redirect(url_for('.index'))


@main.route('/usuarios/<int:user_id>/excluir', methods=['POST'])
def excluir_usuario(user_id):
    user = db.get_or_404(User, user_id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        flash('Usuário removido com sucesso.', 'success')
    else:
        flash('Não foi possível excluir o usuário. Tente novamente.', 'warning')
    return redirect(url_for('.index'))