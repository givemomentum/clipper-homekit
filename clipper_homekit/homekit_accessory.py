import logging

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH
from typing import Any

from pyhap.loader import Loader

logger = logging.getLogger(__name__)


class MicSwitchAccessory(Accessory):
    category = CATEGORY_SWITCH

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        loader = Loader()
        service_switch = loader.get_service("Switch")
        self.add_service(service_switch)
        self.char_on = service_switch.configure_char("On", setter_callback=self.set_on)

    def set_on(self, value: bool):
        self.char_on.set_value(value)
        logger.info(f"Discord Mic: {'[on]' if value else '[off]'}")
