import datetime
import uuid

class Contato:

    id: uuid.UUID
    cliente: uuid.UUID
    descricao: str
    principal: bool
    tipo: str
    ddd: str
    numero: str
    ramal: str
    created_at: datetime.datetime

    def __init__(self) -> None:
        super().__init__()

        self.id = None
        self.cliente = None
        self.descricao = None
        self.principal = None
        self.tipo = None
        self.ddd = None
        self.numero = None
        self.ramal = None
        self.created_at = None
