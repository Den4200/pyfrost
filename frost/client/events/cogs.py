from typing import Any, Dict

from frost.ext import Cog
from frost.client.events.events import messages


class Msgs(Cog, route='messages'):

    def new(data: Dict[str, Any]) -> None:
        messages.new_messages.update(data['msgs'])
