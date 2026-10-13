import requests
from flask import current_app
from . import db
from .models import EmailEnviado


def send_email(to, subject, text):
    """Envia um e-mail pela API HTTP do Mailgun.

    'to' pode ser uma string ou uma lista de e-mails.
    Retorna a resposta do Mailgun.
    """
    destinatarios = ', '.join(to) if isinstance(to, (list, tuple)) else to

    resposta = requests.post(
        current_app.config['MAILGUN_API_URL'],
        auth=('api', current_app.config['MAILGUN_API_KEY']),
        data={
            'from': current_app.config['MAILGUN_FROM'],
            'to': destinatarios,
            'subject': subject,
            'text': text,
        }
    )

    if resposta.status_code == 200:
        current_app.logger.info('[Mailgun] enviado para %s: %s',
                                destinatarios, resposta.text)
    else:
        current_app.logger.error('[Mailgun] falha (%s) para %s: %s',
                                 resposta.status_code, destinatarios,
                                 resposta.text)
    return resposta


def notify_new_user(user, destinatarios):
    """Avisa por e-mail sobre um novo usuário e registra o envio no banco.

    Retorna True se o Mailgun aceitou o e-mail.
    """
    assunto = (current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] +
               ' Novo usuário cadastrado')
    corpo = (
        f"Prontuário: {current_app.config['ALUNO_PRONTUARIO']}\n"
        f"Nome do aluno: {current_app.config['ALUNO_NOME']}\n"
        f'Usuário cadastrado: {user.username}'
    )

    resposta = send_email(destinatarios, assunto, corpo)

    # Registra o envio, para a página "E-mails enviados"
    log = EmailEnviado(
        de=user.username,
        para=', '.join(destinatarios),
        assunto=assunto,
        texto=corpo,
    )
    db.session.add(log)
    db.session.commit()

    return resposta.status_code == 200
