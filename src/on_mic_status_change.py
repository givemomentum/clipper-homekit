import asyncio
import logging
import os
from typing import Callable

import pyautogui

from src.settings import BASE_DIR


logger = logging.getLogger(__name__)


async def on_mic_status_change(callback: Callable[[bool], None]):
    while True:
        is_mic_on = await _is_mic_on()
        callback(is_mic_on)
        await asyncio.sleep(3)


async def _is_mic_on() -> bool:
    try:
        pyautogui.locateOnScreen(
            _get_file_path("mic-on-passively.png"),
            confidence=0.98,
        )
        is_mic_on_passively = True
    except pyautogui.ImageNotFoundException:
        is_mic_on_passively = False

    try:
        pyautogui.locateOnScreen(
            _get_file_path("mic-on-actively.png"),
            confidence=0.98,
        )
        is_mic_on_actively = True
    except pyautogui.ImageNotFoundException:
        is_mic_on_actively = False
    return is_mic_on_passively or is_mic_on_actively


def _get_file_path(file_name: str) -> str:
    return os.path.join(BASE_DIR, "resources", file_name)