# Importando arquivos de configuração
from app.routes import flask_app as application

if __name__ == '__main__':
    application.run(port=80)
