import logging

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH
from typing import Any
from pynput.keyboard import Key, Controller

from pyhap.loader import Loader

from clipper_homekit.on_mic_status_change import is_mic_on


logger = logging.getLogger(__name__)


class MicSwitchAccessory(Accessory):
    category = CATEGORY_SWITCH

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        loader = Loader()
        service_switch = loader.get_service("Switch")
        self.add_service(service_switch)
        self.char_on = service_switch.configure_char("On", setter_callback=self.set_on)

    def set_on(self, value: bool, is_enforce_mic_status: bool = True):
        self.char_on.set_value(value)
        logger.info(f"Discord Mic: {'[on]' if value else '[off]'}")

        if is_enforce_mic_status:
            self.driver.loop.create_task(enforce_mic_status(is_mic_should_be_on=value))


async def enforce_mic_status(is_mic_should_be_on: bool):
    logger.info(f"Enforcing mic status to {'on' if is_mic_should_be_on else 'off'}")

    keyboard = Controller()

    is_mic_on_now = await is_mic_on()
    if is_mic_should_be_on and not is_mic_on_now:
        logger.info("Turning on mic")
        with keyboard.pressed(Key.shift_l, Key.cmd_l):
            keyboard.press("m")
            keyboard.release("m")

    if not is_mic_should_be_on and is_mic_on_now:
        logger.info("Turning off mic")
        with keyboard.pressed(Key.shift_l, Key.cmd_l):
            keyboard.press("m")
            keyboard.release("m")
