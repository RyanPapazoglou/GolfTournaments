import json
from typing import Any
from uuid import UUID

from app.models import Golfers, Users


class GolferEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Golfers):
            return o.to_json()
        elif isinstance(o, UUID):
            return o.hex
        return json.JSONEncoder.default(self, o)

class UsersEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Users):
            return o.to_json()
        elif isinstance(o, UUID):
            return o.hex
        return json.JSONEncoder.default(self, o)