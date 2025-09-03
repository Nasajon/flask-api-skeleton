import datetime
import uuid

from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.descriptor.dto_field_validators import DTOFieldValidators
from nsj_rest_lib.dto.dto_base import DTOBase


@DTO()
class EntityDTO(DTOBase):

    id: uuid.UUID = DTOField(
        pk=True,
        resume=True,
        not_null=True,
        default_value=uuid.uuid4,
        strip=True,
        min=36,
        max=36,
        validator=DTOFieldValidators().validate_uuid,
    )

    escopo: str = DTOField(resume=True, not_null=True, strip=True, min=1, max=100)

    codigo: str = DTOField(resume=True, not_null=True, strip=True, min=1, max=100)

    descricao: str = DTOField(resume=True, not_null=True, strip=True, min=1, max=500)

    json_schema: dict = DTOField(not_null=True)

    content_hash: str = DTOField(not_null=True, strip=True, min=1, max=300)

    created_at: datetime.datetime = DTOField(
        resume=True, not_null=True, default_value=datetime.datetime.now
    )
