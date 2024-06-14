import datetime
import math
import os
import re
import time
from ctypes import cast, POINTER
from datetime import datetime
from datetime import timedelta
from threading import Thread

import pyttsx3
import screen_brightness_control
import speech_recognition as sr
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pygame import mixer

from login import Login
from mr_number import let2num
from mr_vol import average_vol

TIME_SPAN = 12

stop_ascolto = datetime.now()
stop = True
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def esci():
    time.sleep(3)
    os._exit(1)


def vai_in_ascolto():
    if stop:
        beeps[1].play()
        try:
            listen(True)
        except Exception as e:
            print(e)
        return
    def vai_in_sleep():
        while (stop_ascolto - datetime.now()).total_seconds() > 0:
            time.sleep(0.5)
        print('sleep...')
        beeps[2].play()
        global in_ascolto
        in_ascolto = False

    print('in ascolto...')
    beeps[1].play()
    global in_ascolto
    global stop_ascolto
    stop_ascolto = datetime.now() + timedelta(seconds=TIME_SPAN)
    if in_ascolto:
        return
    in_ascolto = True
    Thread(target=vai_in_sleep).start()


def vai_in_sleep():
    global stop_ascolto
    stop_ascolto = datetime.now()


def stop_tutto():
    beeps[2].play(1)
    global stop
    stop = True


def set_brightness(x):
    try:
        num = int(re.search(r'\d+', x[0]).group())
    except:
        num = let2num(x.split('volumea')[1])
    screen_brightness_control.set_brightness(value=num)


def set_volume(x):
    try:
        num = int(re.search(r'\d+', x[0]).group())
    except:
        num = let2num(x.split('volumea')[1])
    db_vol = -63.5
    if not ('muto' in x) and num > 0:
        db_vol = max(-63.5, math.log(num) * 13.7888 - 63.5)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    volume_interface.SetMasterVolumeLevel(db_vol, None)


def goto_learn():
    Login().login_learn()


def rimani_attivo():
    global stop_ascolto
    stop_ascolto += timedelta(days=1)


# This function is from Real Python: https://realpython.com/python-speech-recognition/#putting-it-all-together-a-guess-the-word-game
def recognize_speech_from_mic(recognizer: sr.Recognizer, microphone,force=False) -> dict:
    response = {"success": True,
                "error": None,
                "transcription": None}
    if stop and not force:
        print('Stoppo tutto!')
        return response
    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    avg = 0
    # time.sleep(1)
    with microphone as source:
        while avg < 10:
            if force:
                recognizer.adjust_for_ambient_noise(source,duration=0.5)
            if stop and not force:
                print('Stoppo tutto!')
                return response
            try:
                # beeps[1].play()
                # time.sleep(0.5)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)  # ,timeout=4,phrase_time_limit=4)
            except:
                print('nothing')
                continue
            if force:
                break
            with open('mic.wav', 'wb') as w:
                w.write(audio.get_wav_data())
            avg = average_vol('mic.wav')
            print(avg)

    print('chiamo le api')

    # try recognizing the speech in the recording if a RequestError or UnknownValueError exception is caught, update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='it_IT')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


mixer.init()
beeps = [
    mixer.Sound('raw/beep_in_01.wav'),
    mixer.Sound('raw/beep_in_02.wav'),
    mixer.Sound('raw/beep_out_01.wav')
]
start_recognizer = [
    'heymistersun',
    'emystoreseregno',
    'emistersun',
    'heymrsun',
    'mistersun',
    'mrsanders',
    'imistersun',
    'emistersandro',
    'emi60',
    'iniziadettatura',
    'iniziodettatura',
    'ascolta',
    'ascoltami',
    'ascolti',
    'ascolto'
]
my_phrases = [
    [['ciao'], 'Ciao, come stai?', None],
    [['chisei'], 'Sono mister san.', None],
    [['cheor'], None,
     lambda x: x[1].say('Sono le ' + datetime.now().strftime('%HH e %MM').lower().replace('h', '').replace('m', ''))],

    [['esci'], 'Mister san si sta chiudendo...', lambda _: esci()],
    [['luminosit'], None, lambda x: set_brightness(x)],
    [['volume'], None, lambda x: set_volume(x)],
    [['universit', 'learnlogin', 'learn'], None, lambda x: goto_learn()],
    [['rimaniattivo', 'rimaniinascolto'], 'Rimango attivo', lambda _: rimani_attivo()],
    [['disattivati', 'nonmiascoltare', 'sleep'], 'Vado in sleep', lambda _: vai_in_sleep()],

    [['obs', 'ubs', 'regestratore','ovs'], None, lambda _: os.startfile('links\obs.lnk')],
    [['team', 'microsoft', 'riunion'], None, lambda _: os.startfile('links\Microsoft Teams (work or school).lnk')],
    [['mozil', 'browser', 'firef'], None, lambda _: os.startfile('links\Firefox.lnk')],
    [['esplor'], None, lambda _: os.startfile('links\File Explorer.lnk')],
    [['studio', 'visual'], None, lambda _: os.startfile('links\Visual Studio 2022 (2).lnk')]
]
unknown_command_phrase = ["Non ho capito", None]

def new_voice():
    engine = pyttsx3.init()
    it_voice_id_m = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_IT-IT_COSIMO_11.0"
    engine.setProperty('voice', it_voice_id_m)
    engine.setProperty('rate', 175)
    return engine

engine = new_voice()

in_ascolto = False


def listen(force=False):
    response = recognize_speech_from_mic(recognizer, microphone,force)

    transcription: str = response['transcription']
    if transcription is None:
        return
    transcription = re.sub(r'\W+', '', transcription).strip().lower()
    print(f'--> {transcription} <--')
    if transcription in start_recognizer:
        vai_in_ascolto()
        return
    if not in_ascolto and not force:
        print('ignoro perchè sono in sleep...')
        return
    print('sto per processare: ...')
    global stop_ascolto
    stop_ascolto += timedelta(seconds=TIME_SPAN)
    for keys, answer, action in my_phrases:
        for key in keys:
            if key in transcription:
                beeps[0].play()
                if answer is not None:
                    engine.say(answer)
                if action is not None:
                    Thread(target=action, args=[[transcription,engine]]).start()

                break


def mr_rec_start():
    global stop
    stop=False

    # beeps[1].play(1)
    # engine.say("Mister san si sta avviando...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        if not stop:
            listen()
        else:
            time.sleep(3)
