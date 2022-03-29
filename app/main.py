# Importando arquivos de configuração
from app.settings import flask_app
import app.db_pool_config

# Importando os controllers
import app.controller.clientes_controller

if __name__ == '__main__':
    flask_app.run(port=5000)
