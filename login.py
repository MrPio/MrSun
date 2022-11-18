import time
import webbrowser

import pyautogui
from pynput.keyboard import Controller

from mr_crypto import MrCrypto


class Login():

    def __wait_for_element_appear(self, element_path: str, wait=8.0, confidence=0.7, grayscale=False):
        start = time.time()
        while True:
            element = pyautogui.locateOnScreen(element_path, grayscale=grayscale, confidence=confidence)
            if time.time() - start > wait:
                print(f"I've waited too much! [{element_path}]")
                return None
            pyautogui.sleep(0.5)
            if element is not None:
                break
        return element


    def __click_center(self, element):
        pyautogui.click(x=element.left + int(element.width / 2),
                        y=element.top + int(element.height / 2))

    def login_learn(self):
        try:
            keyboard = Controller()
            mc = MrCrypto()
            pyautogui.hotkey('win', 'd')
            pyautogui.sleep(0.05)
            webbrowser.open('https://learn.univpm.it/', new=2)
            pyautogui.sleep(0.6)
            self.__wait_for_element_appear('screens/learn_01.png')

            for i in range(3):
                pyautogui.press("tab")
            pyautogui.press("enter")

            self.__wait_for_element_appear('screens/learn_03.png')

            keyboard.type(mc.decrypt('gAAAAABjdtRlNRhLhrBf23UFRNw4KzJbRIlMiAT9_hNMcMPr4xui9PCTiyWCRhHKRox0yFZEsRK4nMHs_MW3Y5Je3OD3yiARdQ=='))
            pyautogui.press("tab")
            keyboard.type(mc.decrypt('gAAAAABjdtRl4COR-3dqr9xHBjTBCPUb0oIIDweN-lUFBmnXH8VgynRj1de8AbbuV8m5B2aF5CtGRvzMnmG3MBV1GCrl25sXYg=='))
            pyautogui.press("enter")
        except Exception as e:
            print(e)
