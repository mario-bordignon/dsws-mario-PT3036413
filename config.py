import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Carrega o .env usando o caminho absoluto do projeto,
# funcionando não importa de onde o Flask for iniciado
load_dotenv(os.path.join(basedir, '.env'), override=True)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chaveultrasecreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Mailgun (valores vêm do .env) ---
    MAILGUN_API_URL = os.environ.get('MAILGUN_API_URL')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_FROM = os.environ.get('MAILGUN_FROM')
    FLASKY_MAIL_SUBJECT_PREFIX = '[DSWS]'

    # --- Dados da atividade avaliativa ---
    ALUNO_PRONTUARIO = 'PT3036413'
    ALUNO_NOME = 'Mario Bordignon'

    # Recebem o aviso sempre, a cada novo usuário
    FLASKY_DESTINATARIOS_FIXOS = [
        'm.bordignon@aluno.ifsp.edu.br',
    ]

    # Só recebe se a caixa de seleção estiver marcada.
    # Para trocar a conta usada, mude só o número abaixo:
    #   '1' -> usa FLASKY_CAIXA1
    #   '2' -> usa FLASKY_CAIXA2
    FLASKY_CAIXA_TESTE = '2'
    FLASKY_CAIXA = os.environ.get(f'FLASKY_CAIXA{FLASKY_CAIXA_TESTE}')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
