import math
import os
import random
import time
from ctypes import cast, POINTER

import pyautogui
import pygame
import screen_brightness_control
import win32api
import winotify
from comtypes import CLSCTX_ALL
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.utils import AudioUtilities

from mr_rec import vai_in_ascolto, beeps

UI_DIR = os.path.dirname(os.path.abspath(__file__))


def set_volume(num):
    db_vol = -63.5
    if num > 0:
        db_vol = max(-63.5, math.log(num) * 13.7888 - 63.5)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    try:
        volume_interface.SetMasterVolumeLevel(db_vol, None)
    except:
        pass


def set_brightness(num):
    screen_brightness_control.set_brightness(value=num)


def notifica(titolo: str, contenuto: str, icon) -> None:
    notifica = winotify.Notification(
        app_id='MrSun',
        title=titolo,
        msg=contenuto,
        icon=icon,
        duration='short',
    )
    notifica.set_audio(winotify.audio.Default, False)
    notifica.show()


def press_special_key(code):
    # codes: https://docs.microsoft.com/it-it/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
    hwcode = win32api.MapVirtualKey(code, 0)
    win32api.keybd_event(code, hwcode)


def mute_key():
    press_special_key(0xAD)


def volume_down_key():
    press_special_key(0xAE)


def volume_up_key():
    press_special_key(0xAF)


def prev_trak_key():
    press_special_key(0xB1)


def next_trak_key():
    press_special_key(0xB0)


def play_pause_key():
    press_special_key(0xB3)

def mr_wii_start():
    last_command = time.time_ns()
    pygame.init()
    j = None
    try:
        j = pygame.joystick.Joystick(0)
    except pygame.error:  # This bit doesn't seem to work properly.
        print("Joystick not connected.")
    j.init()

    axis_1_mode = True
    arrows_mode = True
    while 1:
        pygame.event.pump()

        axis_0 = (j.get_axis(0) + 1) / 2.0
        axis_1 = (j.get_axis(1) + 1) / 2.0

        angle_norm=-(math.atan2(j.get_axis(0),j.get_axis(1))-math.pi)/(2*math.pi)
        if angle_norm > 0.9 or angle_norm<0.10:
            angle_norm = 0
        elif angle_norm<0.10:
            angle_norm=0
        else:
            angle_norm=(angle_norm-0.1)/0.8
        radius = math.sqrt(j.get_axis(0)**2 + j.get_axis(1)**2)

        if radius > 0.88:
            if axis_1_mode:
                set_volume(angle_norm * 100)
            else:
                set_brightness(100-(angle_norm * 100))

        if round(j.get_axis(2)) == -1:  # Up key
            if arrows_mode:
                pyautogui.hotkey('ctrl', 'win', 'left')
            else:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
        elif round(j.get_axis(2)) == 1:  # Down key
            if arrows_mode:
                pyautogui.hotkey('ctrl', 'win', 'right')
            else:
                pyautogui.hotkey('ctrl', 'tab')
        elif round(j.get_axis(3)) == -1:  # Right
            if arrows_mode:
                pyautogui.hotkey('ctrl', 'win', 'd')
            else:
                pyautogui.hotkey('ctrl', 'shift', 't')
        elif round(j.get_axis(3)) == 1:  # Left
            if arrows_mode:
                pyautogui.hotkey('ctrl', 'win', 'f4')
            else:
                pyautogui.hotkey('ctrl', 'w')

        b_down=False

        if j.get_button(0):  # ButtonA
            if time.time_ns() - last_command < 350_000_000:
                continue
            last_command = time.time_ns()
            play_pause_key()
        if j.get_button(1):  # B
            b_down=True
        if j.get_button(2):  # A
            if time.time_ns() - last_command < 95_000_000:
                continue
            last_command = time.time_ns()
            volume_up_key()
        if j.get_button(3):  # 2
            if time.time_ns() - last_command < 95_000_000:
                continue
            last_command = time.time_ns()
            volume_down_key()
        if j.get_button(4):  # Plus
            if time.time_ns() - last_command < 500_000_000:
                continue
            last_command=time.time_ns()
            vai_in_ascolto()
        if j.get_button(5):  # Minus
            if time.time_ns() - last_command < 500_000_000:
                continue
            last_command = time.time_ns()

            if b_down:
                arrows_mode = not arrows_mode
                if arrows_mode:
                    notifica('ARROWS --> WINDOWS', 'Hai selezionato il controllo delle tabs di firefox.',
                             UI_DIR + '/ico/explorer.png')
                else:
                    notifica('ARROWS --> FIREFOX', 'Hai selezionato il controllo dei desktop virtuali.', UI_DIR + '/ico/firefox.png')
            else:
                axis_1_mode = not axis_1_mode
                if axis_1_mode:
                    notifica('PAD --> VOLUME', 'Hai selezionato il controllo del volume.', UI_DIR + '/ico/sound.ico')
                else:
                    notifica('PAD --> LUMINOSITA', 'Hai selezionato il controllo della luminosità.',
                             UI_DIR + '/ico/brightness.ico')

            print(5)
        if j.get_button(6):  # -
            if time.time_ns() - last_command < 120_000_000:
                continue
            last_command = time.time_ns()
            next_trak_key()
        if j.get_button(7):  # +
            if time.time_ns() - last_command < 120_000_000:
                continue
            last_command = time.time_ns()
            prev_trak_key()
        if j.get_button(8):  # Home
            print(8)
        if j.get_button(9):  # Home
            print(9)
        if j.get_button(10):  # Home
            print(10)

        time.sleep(0.05)

if __name__=='__main__':
    mr_wii_start()