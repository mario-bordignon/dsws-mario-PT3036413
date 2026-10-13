from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('Qual o seu nome?', validators=[DataRequired()])
    enviar_caixa = BooleanField('Deseja enviar e-mail?')
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O endereço vem da configuração, que só existe com o app ativo
        self.enviar_caixa.label.text = (
            f"Deseja enviar e-mail para {current_app.config['FLASKY_CAIXA']}?"
        )
