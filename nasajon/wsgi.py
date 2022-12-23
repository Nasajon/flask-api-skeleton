# Importando arquivos de configuração
from nasajon.settings import application
import nasajon.db_pool_config

# TODO Importar todos os controllers (se não, as rotas não existirão)
import nasajon.controller.cliente_controller
import nasajon.controller.ping_controller
import nasajon.controller.token_info_controller
import nasajon.controller.async_order_controller

if __name__ == '__main__':
    application.run(port=5000)
