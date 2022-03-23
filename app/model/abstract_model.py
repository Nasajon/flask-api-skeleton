from abc import ABC
from nsj_gcf_utils.json_util import json_dumps, json_loads
from typing import Any, Dict


class AbstractModel(ABC):

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json_dumps(self.to_dict())

    def load_from_dict(self, obj: Dict[str, Any]):
        for k in obj:
            if (hasattr(self, k)):
                setattr(self, k, obj[k])

    def load_from_json(self, json: str):
        obj = json_loads(json)
        return self.from_dict(obj)
