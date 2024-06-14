import os
from threading import Thread

import pystray
import screen_brightness_control
from PIL import Image


def set_brightness(value):
    print(value)
    global screen_brightness
    screen_brightness = value
    screen_brightness_control.set_brightness(value=value)


screen_brightness = screen_brightness_control.get_brightness()


def start_tray():
    pystray.Icon(
        'MrSun',
        Image.open("icon.ico"),
        menu=pystray.Menu(
            pystray.MenuItem('Brightness MAX', lambda: set_brightness(100), radio=True,
                             checked=lambda _: screen_brightness == 100),
            pystray.MenuItem(f'Brightness {90}', lambda: set_brightness(90), radio=True,
                             checked=lambda _: screen_brightness == 90),
            pystray.MenuItem(f'Brightness {80}', lambda: set_brightness(80), radio=True,
                             checked=lambda _: screen_brightness == 80),
            pystray.MenuItem(f'Brightness {70}', lambda: set_brightness(70), radio=True,
                             checked=lambda _: screen_brightness == 70),
            pystray.MenuItem(f'Brightness {60}', lambda: set_brightness(60), radio=True,
                             checked=lambda _: screen_brightness == 60),
            pystray.MenuItem(f'Brightness {50}', lambda: set_brightness(50), radio=True,
                             checked=lambda _: screen_brightness == 50),
            pystray.MenuItem(f'Brightness {40}', lambda: set_brightness(40), radio=True,
                             checked=lambda _: screen_brightness == 40),
            pystray.MenuItem(f'Brightness {30}', lambda: set_brightness(30), radio=True,
                             checked=lambda _: screen_brightness == 30),
            pystray.MenuItem(f'Brightness {20}', lambda: set_brightness(20), radio=True,
                             checked=lambda _: screen_brightness == 20),
            pystray.MenuItem(f'Brightness {10}', lambda: set_brightness(10), radio=True,
                             checked=lambda _: screen_brightness == 10),
            pystray.MenuItem('Brightness MIN', lambda: set_brightness(0), radio=True,
                             checked=lambda _: screen_brightness == 0),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', lambda: os._exit(1), default=True),
            pystray.Menu.SEPARATOR,
        )
    ).run()


if __name__ == '__main__':
    Thread(target=start_tray).start()
