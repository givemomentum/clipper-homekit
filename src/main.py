import logging
import signal

from pyhap.accessory_driver import AccessoryDriver
import asyncio

from src.homekit_accessory import MicSwitchAccessory
from src.on_mic_status_change import on_mic_status_change


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    driver = AccessoryDriver(port=51826)
    signal.signal(signal.SIGTERM, driver.signal_handler)

    mic_accessory = MicSwitchAccessory(driver=driver, display_name="Discord Mic")
    driver.add_accessory(accessory=mic_accessory)

    mic_monitor_task = asyncio.create_task(
        on_mic_status_change(lambda is_mic_on: mic_accessory.set_on(is_mic_on))
    )

    try:
        await driver.async_start()
        logging.info("Driver started")
        while True:
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received")
        mic_monitor_task.cancel()
        await mic_monitor_task
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
    finally:
        logging.info("Main coroutine exiting")


if __name__ == "__main__":
    asyncio.run(main())
