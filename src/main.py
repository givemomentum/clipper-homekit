from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_SWITCH
from pyhap.loader import Loader


class MicSwitchAccessory(Accessory):
    category = CATEGORY_SWITCH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loader = Loader()
        service_switch = loader.get_service("Switch")
        self.add_service(service_switch)
        self.char_on = service_switch.configure_char("On", setter_callback=self.set_on)

    def set_on(self, value):
        # Implement the logic to turn your socket on or off
        print("Turning the Discord Mic on" if value else "Turning the Discord Mic off")


def init():
    driver = AccessoryDriver(port=51826)
    mic_accessory = MicSwitchAccessory(driver=driver, display_name="Mic Switch")
    driver.add_accessory(accessory=mic_accessory)
    driver.start()


if __name__ == "__main__":
    init()
