# TTS plugin for pyttsx3 engine
# author: Vladislav Janvarev

import os

from vacore import VACore
import pyttsx3

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "TTS pyttsx",
        "version": "1.1",
        "require_online": False,

        "description": """
TTS через pyttsx.
Обычно работает без проблем, если у вас Windows с русским языком; иначе лучше переставить engineId на vosk или silero_v3.
""",

        "default_options": {
            "sysId": 0, # id голоса в системе (резервный)
            "rate": 150, # скорость речи
            "volume": 0.9, # громкость
        },

        "tts": {
            "pyttsx": (init,say,towavfile) # первая функция инициализации, вторая - говорить, третья - в wav file
                                            # если вторая - None, то используется 3-я с проигрыванием файла
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def init(core:VACore):
    options = core.plugin_options(modname)

    core.ttsEngine = pyttsx3.init()

    """
    Установка голоса по умолчанию (индекс может меняться в зависимости от настроек операционной системы)
    """


    voices = core.ttsEngine.getProperty("voices")
    
    print(f"PyTTSx: Найдено голосов: {len(voices)}")
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.id} - {voice.name} ({voice.languages})")

    # if assistant.speech_language == "en":
    #     assistant.recognition_language = "en-US"
    #     if assistant.sex == "female":
    #         # Microsoft Zira Desktop - English (United States)
    #         ttsEngine.setProperty("voice", voices[1].id)
    #     else:
    #         # Microsoft David Desktop - English (United States)
    #         ttsEngine.setProperty("voice", voices[2].id)
    # else:
    #     assistant.recognition_language = "ru-RU"

    # Ищем лучший русский женский голос
    best_voice_index = options["sysId"]
    for i, voice in enumerate(voices):
        voice_info = str(voice.languages).lower() + " " + str(voice.name).lower()
        if any(lang in voice_info for lang in ["russian", "ru", "русский", "рус"]):
            if any(gender in voice_info for gender in ["female", "женский", "жен"]):
                best_voice_index = i
                print(f"PyTTSx: Найден русский женский голос: {voice.name}")
                break
            else:
                best_voice_index = i
                print(f"PyTTSx: Найден русский голос: {voice.name}")
                break
    
    # Устанавливаем голос и параметры
    core.ttsEngine.setProperty("voice", voices[best_voice_index].id)
    core.ttsEngine.setProperty("rate", options.get("rate", 150))
    core.ttsEngine.setProperty("volume", options.get("volume", 0.9))
    
    print(f"PyTTSx: Использую голос: {voices[best_voice_index].name}")
    print(f"PyTTSx: Скорость: {options.get('rate', 150)}, Громкость: {options.get('volume', 0.9)}")

def say(core:VACore, text_to_speech:str):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    core.ttsEngine.say(str(text_to_speech))
    core.ttsEngine.runAndWait()

def towavfile(core:VACore, text_to_speech:str,wavfile:str):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    core.ttsEngine.save_to_file(str(text_to_speech),wavfile)
    core.ttsEngine.runAndWait()