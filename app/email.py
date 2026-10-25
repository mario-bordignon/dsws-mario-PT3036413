import requests
from flask import current_app


def send_email(to, subject, text):
    """Envia um e-mail pela API HTTP do Mailgun para um destinatário.

    Retorna a resposta do Mailgun.
    """
    resposta = requests.post(
        current_app.config['MAILGUN_API_URL'],
        auth=('api', current_app.config['MAILGUN_API_KEY']),
        data={
            'from': current_app.config['MAILGUN_FROM'],
            'to': to,
            'subject': subject,
            'text': text,
        }
    )

    if resposta.status_code == 200:
        current_app.logger.info('[Mailgun] enviado para %s: %s', to, resposta.text)
    else:
        current_app.logger.error('[Mailgun] falha (%s) para %s: %s',
                                 resposta.status_code, to, resposta.text)
    return resposta


def notify_new_user(user, email_usuario):
    """Avisa por e-mail sobre um novo usuário.

    Envia para os destinatários fixos e para o e-mail digitado no formulário.
    Cada envio é separado, assim um endereço não autorizado no sandbox do
    Mailgun não impede os demais.

    Retorna um dicionário {endereço: True/False} com o resultado de cada envio.
    """
    assunto = (current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] +
               ' Novo usuário cadastrado')
    corpo = (
        f"Prontuário: {current_app.config['ALUNO_PRONTUARIO']}\n"
        f"Nome do aluno: {current_app.config['ALUNO_NOME']}\n"
        f'Usuário cadastrado: {user.username}'
    )

    destinatarios = list(current_app.config['FLASKY_DESTINATARIOS_FIXOS'])
    email_usuario = email_usuario.strip()
    if email_usuario.lower() not in [d.lower() for d in destinatarios]:
        destinatarios.append(email_usuario)

    resultados = {}
    for destinatario in destinatarios:
        resposta = send_email(destinatario, assunto, corpo)
        resultados[destinatario] = resposta.status_code == 200
    return resultados