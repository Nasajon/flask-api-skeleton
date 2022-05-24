# Importando arquivos de configuração
import os

# import debugpy
from nasajon.settings import application
import nasajon.db_pool_config

# TODO Importar todos os controllers (se não, as rotas não existirão)
import nasajon.controller.clientes_controller
import nasajon.controller.token_info_controller
import ptvsd
ptvsd.enable_attach(("0.0.0.0",9000))
# debugpy.configure(python="/usr/bin/python3")
# debugpy.listen(("0.0.0.0",9000))
if __name__ == '__main__':
    application.run(port=5000,debug=True)
    