import os
from threading import Thread

import pystray
import screen_brightness_control
from PIL import Image

from mr_wii import mr_wii_start


def set_brightness(value):
    return screen_brightness_control.set_brightness(value=value)


def get_brightness():
    return screen_brightness_control.get_brightness()


def on_exit(icon, item):
    if str(item) == 'Exit':
        os._exit(1)

    elif str(item) == 'Brightness + 10':
        set_brightness(min(100, get_brightness()[0] + 10))
    elif str(item) == 'Brightness - 10':
        set_brightness(max(0, get_brightness()[0] - 10))

    elif str(item) == 'Brightness + 20':
        set_brightness(min(100, get_brightness()[0] + 20))
    elif str(item) == 'Brightness - 20':
        set_brightness(max(0, get_brightness()[0] - 20))

    elif str(item) == 'Brightness + 30':
        set_brightness(min(100, get_brightness()[0] + 30))
    elif str(item) == 'Brightness - 30':
        set_brightness(max(0, get_brightness()[0] - 30))

    elif str(item) == 'Brightness + 50':
        set_brightness(min(100, get_brightness()[0] + 50))
    elif str(item) == 'Brightness - 50':
        set_brightness(max(0, get_brightness()[0] - 50))

    elif str(item) == 'Brightness MAX':
        set_brightness(100)
    elif str(item) == 'Brightness MIN':
        set_brightness(0)

    elif str(item) == 'Listen':
        vai_in_ascolto()
    elif str(item) == 'Stop Listen':
        vai_in_sleep()


def start_tray():
    # icon_folder = os.path.join(sys._MEIPASS, 'icon')
    # icon_path=icon_folder + "\icon.ico"
    pystray.Icon(
        'MrSun',
        Image.open("icon.ico"),
        menu=pystray.Menu(
            pystray.MenuItem(
                'Brightness + 10', on_exit
            ),
            pystray.MenuItem(
                'Brightness - 10', on_exit
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                'Brightness + 20', on_exit
            ),
            pystray.MenuItem(
                'Brightness - 20', on_exit
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                'Brightness + 30', on_exit
            ),
            pystray.MenuItem(
                'Brightness - 30', on_exit
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                'Brightness + 50', on_exit
            ),
            pystray.MenuItem(
                'Brightness - 50', on_exit
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                'Brightness MAX', on_exit
            ),
            pystray.MenuItem(
                'Brightness MIN', on_exit
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                'Listen', on_exit,default=True
            ),
            pystray.MenuItem(
                'Stop Listen', on_exit
            ),
            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                'Exit', on_exit
            ),
        )
    ).run()

if __name__=='__main__':
    Thread(target=start_tray).start()
    Thread(target=mr_wii_start).start()

    from mr_rec import mr_rec_start, vai_in_sleep, vai_in_ascolto

    mr_rec_start()