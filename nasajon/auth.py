from nsj_flask_auth import Auth, Scope
from nasajon.settings import DIRETORIO_URL, PROFILE_URL, API_KEY

auth = Auth(DIRETORIO_URL, PROFILE_URL, API_KEY,
            scope=Scope.GRUPO_EMPRESARIAL)
