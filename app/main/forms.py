from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    email = StringField(
        'Qual é o seu email (Envio de notificação do novo usuário)?',
        validators=[
            DataRequired(),
            Length(max=254),
            Regexp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$',
                   message='Digite um e-mail válido.'),
        ])
    submit = SubmitField('Submit')


class EditUserForm(FlaskForm):
    """Edição do nome, feita na própria linha da tabela de usuários."""
    name = StringField('Nome do usuário', validators=[
        DataRequired(message='Digite o nome do usuário.'),
        Length(max=64, message='O nome pode ter no máximo 64 caracteres.'),
    ])
    submit = SubmitField('Salvar')


class DeleteForm(FlaskForm):
    """Formulário vazio, usado só para proteger a exclusão com o token CSRF."""
    submit = SubmitField('Excluir')