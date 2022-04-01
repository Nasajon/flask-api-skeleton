# Importando arquivos de configuração
from app.settings import flask_app
import app.db_pool_config

# TODO Importar todos os controllers (se não, as rotas não existirão)
import app.controller.clientes_controller
import app.controller.token_info_controller

if __name__ == '__main__':
    flask_app.run(port=5000)
