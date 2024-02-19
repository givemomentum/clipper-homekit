import argparse
import asyncio
import logging
import signal

from pyhap.accessory_driver import AccessoryDriver

from clipper_homekit.homekit_accessory import MicSwitchAccessory
from clipper_homekit.on_mic_status_change import on_mic_status_change


logging.basicConfig(level=logging.INFO)
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)


async def start_server(is_monitor_mic: bool = True) -> None:
    loop = asyncio.get_running_loop()
    driver = AccessoryDriver(loop=loop)
    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(driver.stop()))

    mic_accessory = MicSwitchAccessory(driver=driver, display_name="Discord Mic Switch")
    driver.add_accessory(accessory=mic_accessory)

    tasks = []
    if is_monitor_mic:
        mic_monitor_task = asyncio.create_task(
            on_mic_status_change(lambda is_mic_on: mic_accessory.set_on(is_mic_on))
        )
        tasks.append(mic_monitor_task)

    server_task = asyncio.create_task(driver.async_start())
    tasks.append(server_task)

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
    finally:
        await driver.stop()
        logging.info("Main coroutine exiting")


def main():
    parser = argparse.ArgumentParser("clipper_homekit_server")
    parser.add_argument(
        "--monitor-mic",
        default=True,
        dest="is_monitor_mic",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--debug",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    asyncio.run(start_server(is_monitor_mic=args.is_monitor_mic))
